from datetime import datetime, timedelta, date

from dateutil.tz import gettz
import re

from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, abort
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException

import app
from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm, \
    MessageForm, \
    PilotKommt, PilotGeht, PilotIndex, MyDTPForm

from app.models import User, Post#, Message, Notification
from app.models import PilotLog
from app.translate import translate
from app.main import bp

from astral.sun import sun
from astral import LocationInfo

def sunset(day: date = None):
    sunsetDay = day or datetime.utcnow()
    myLocation = LocationInfo('name', 'region', app.Config.LOC_TZ, app.Config.LATITUDE, app.Config.LONGITUDE)
    s = sun(myLocation.observer, date=sunsetDay, tzinfo=myLocation.timezone)
    return s["sunset"]#.strftime('%H:%M')

def tAbrund10(dt: datetime):
    m = round(dt.minute, -1)
    if m >= dt.minute:
        m = m-10
    rdt = dt.replace(minute=m, second=0, microsecond=0)
    return rdt

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        # g.search_form = SearchForm()
    g.locale = str(get_locale())
    g.site_prefix = current_app.config['SITE_PREFIX']
    g.fbversion = current_app.config['FB_VERSION']


# @bp.route('/', methods=['GET', 'POST'])
# @bp.route('/index', methods=['GET', 'POST'])
@login_required
def old_index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/meldung', methods=['GET', 'POST'])
@login_required
def meldung():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language, timestamp=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash(_('Neue Meldung gespeichert'))
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id=current_user.id).first_or_404()
    # page = request.args.get('page', 1, type=int)
    # pLogs = PilotLog.query.order_by(PilotLog.start.desc()) #.filter_by((PilotLog.start >= date.today())).order_by(PilotLog.start.desc())
    pLogs = user.piLogs.filter(PilotLog.start >= date.today()).order_by(PilotLog.start.desc()).all()
    today = date.today().strftime('%Y-%m-%d')

    return render_template('pilot_meldung.html', user=user, pLogs=pLogs, todate=today,
                           form=form)

@bp.route('/loginPilot', methods=['GET', 'POST'])
@login_required
def loginPilot():
    form = PilotKommt()
    tm = datetime.utcnow().replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
    # auf 10 Minuten abgerundet
    tm = tm - timedelta(minutes=tm.minute % 10,
                                 seconds=tm.second,
                                 microseconds=tm.microsecond)

    # get current user login and convert start and stoptime to local TZ
    currUlog = current_user.get_active_log()
    if currUlog and currUlog.start:
        # deal with local time zone for start time
        currUlog.start = currUlog.start.replace(tzinfo=gettz('UTC'))#.astimezone(gettz(current_app.config['LOC_TZ']))
        print("currUlog.start1 = "+currUlog.start.isoformat(timespec='seconds'))
    if currUlog and currUlog.stop:
        # deal with local time zone for stop time
        currUlog.stop = currUlog.stop.replace(tzinfo=gettz('UTC'))#.astimezone(gettz(current_app.config['LOC_TZ']))

    # get current Flugleiter login and convert start and stoptime to local TZ
    currFLlog = PilotLog.query.filter(PilotLog.start >= date.today()). \
        filter(PilotLog.flugleiter == 1).filter(PilotLog.stop == None).order_by(PilotLog.start.desc()).first()
    if currFLlog and currFLlog.start:
        # deal with local time zone for start time
        currFLlog.start = currFLlog.start.replace(tzinfo=gettz('UTC'))#.astimezone(gettz(current_app.config['LOC_TZ']))
        print("currFLlog.start = "+currFLlog.start.isoformat(timespec='seconds'))
    if currFLlog and currFLlog.stop:
        # deal with local time zone for stop time
        currFLlog.stop = currFLlog.stop.replace(tzinfo=gettz('UTC'))#.astimezone(gettz(current_app.config['LOC_TZ']))

    if form.validate_on_submit():
        print("form.zeitKommt = "+form.zeitKommt.data)
        print(f'form.flugleiter = {form.flugleiter.data}')
        if form.flugleiter.data:
            rolle = 'Flugleiter'
        else:
            rolle= 'Pilot'
        flash(f'Hallo {current_user.first_name}, Du hast Dich um {form.zeitKommt.data} Uhr als {rolle} angemeldet.')
        kommtUTC = datetime.strptime(datetime.strftime(tm, '%Y-%m-%d ')+form.zeitKommt.data,
                                    '%Y-%m-%d %H:%M')
        print("form.zeitKommt2 = "+kommtUTC.isoformat(timespec='seconds'))
        kommtUTC = kommtUTC.replace(tzinfo=gettz(current_app.config['LOC_TZ'])).astimezone(gettz('UTC'))
        print("form.zeitKommt3 = "+kommtUTC.isoformat(timespec='seconds'))
        if currUlog == None:
            newPiLog = PilotLog(user_id=current_user.id, start=kommtUTC,
                          flugleiter=form.flugleiter.data)
            db.session.add(newPiLog)
        else: # Wenn Flugleiterattribut geändert wurde, aktuellen Log abschließen und neuen Log anfangen
            if currUlog.flugleiter != form.flugleiter.data:
                newPiLog = PilotLog(user_id=current_user.id, start=kommtUTC,
                                 flugleiter=form.flugleiter.data)
                db.session.add(newPiLog)
                print("currUlog.start2 = "+currUlog.start.isoformat(timespec='seconds'))
                print("piLog.start = "+newPiLog.start.isoformat(timespec='seconds'))
                print(currUlog.start > newPiLog.start)
                if currUlog.start > newPiLog.start:
                    currUlog.stop = currUlog.start
                else:
                    print("piLog.start in else= " + newPiLog.start.isoformat(timespec='seconds'))
                    currUlog.stop = newPiLog.start
                    print("currUlog.stop in else= " + currUlog.stop.isoformat(timespec='seconds'))
            else:
                currUlog.start = kommtUTC

        # Ablösung Flugleiter, wenn notwendig
        if form.flugleiter.data and currFLlog and currFLlog.pilot.id != current_user.id:
          currFLlog.stop = kommtUTC
          newPiLog = PilotLog(user_id=currFLlog.pilot.id, start=kommtUTC,
                              flugleiter=False)
          db.session.add(newPiLog)

        if currUlog:
            # Hack um Fehler mit Zeitzone zu vermeiden:
            currUlog.start = currUlog.start.astimezone(gettz('UTC'))
            # Check:
            print('vor Commit: currUlog.id = '+str(currUlog.id))
            print("currUlog.start = "+currUlog.start.isoformat(timespec='seconds'))
            if currUlog.stop:
                print("currUlog.stop = ",currUlog.stop.isoformat(timespec='seconds'))
            else:
                print("currUlog.stop = None")
        db.session.commit()
        return redirect('/pilotIndex')


    if currUlog != None:
        if currUlog.flugleiter:
            rolle = 'Flugleiter'
            nrolle = 'Pilot'
        else:
            nrolle = 'Flugleiter'
            rolle = 'Pilot'

        flash(f'Hallo {current_user.first_name}, Du hast Dich um '+
              f'{currUlog.start.astimezone(gettz(current_app.config["LOC_TZ"])).strftime("%H:%M")} Uhr '+
              f'als {rolle} angemeldet.')
        flash('Möchtest Du deine Ankunftszeit ändern '+
              f'oder möchtest Du Dich als {nrolle} anmelden?'
           )

    print(sunset())
    return render_template('pilot_kommt.html', title=_('Anmeldung Flugprotokoll'),
                           form=form, stime=tm, sunset=sunset())

    # return render_template('pilot_kommt.html', form=form)

@bp.route('/logoffPilot', methods=['GET', 'POST'])
@login_required
def logoffPilot():
    form = PilotGeht()
    tm = datetime.now()
    tm = tm - timedelta(minutes=tm.minute % 10,
                                 seconds=tm.second,
                                 microseconds=tm.microsecond)
    print(tm)
    if form.validate_on_submit():
        gehtDO = datetime.strptime(datetime.strftime(tm, '%Y-%m-%d ')+form.zeitGeht.data,
                                    '%Y-%m-%d %H:%M')
        gehtDO = gehtDO.replace(tzinfo=gettz(current_app.config['LOC_TZ'])).astimezone(gettz('UTC'))

        piLog = current_user.get_active_log()
        if piLog:
          piLog.start = piLog.start.replace(tzinfo=gettz('UTC'))
          if piLog.start > gehtDO:
              gehtDO = piLog.start

          piLog.set_geht(gehtDO)
          # db.session.add(piLog)
          db.session.commit()
        else:
          flash('Hallo {}, Du bist bereits abgemeldet.'.format(
              current_user.first_name))
        return redirect('/pilotIndex')

    currUlog = current_user.get_active_log()
    if currUlog and currUlog.start:
        currUlog.start = currUlog.start.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
        print("currUlog.start = "+currUlog.start.isoformat(timespec='seconds'))
    if currUlog and currUlog.stop:
        currUlog.stop = currUlog.stop.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
    if currUlog == None:
        flash('Hallo {}, Du bist derzeit nicht aktiv angemeldet.'.format(
            current_user.first_name))
    else:
        flash('Hallo {}, Du hast Dich um {} Uhr angemeldet.'.format(
            current_user.first_name, currUlog.start.strftime('%H:%M')))

    return render_template('pilot_geht.html', title=_('Abmeldung Flugprotokoll'),
                           form=form, stime=tm, currPiLog=currUlog)
    # return render_template('pilot_kommt.html', form=form)

@bp.route('/')
@bp.route('/index')
@bp.route('/pilotIndex')
@login_required
def index():
    import copy
    # piData = PilotIndex()
    # print(piData)
    user = User.query.filter_by(id=current_user.id).first_or_404()
    # page = request.args.get('page', 1, type=int)
    pLogs = user.piLogs.filter(PilotLog.start >= date.today()).order_by(PilotLog.id.desc()).all()
    pPosts = user.posts.filter(Post.timestamp >= date.today()).order_by(Post.timestamp).all()

    pPosts2=[]
    for post in pPosts:
      # print("post.timestamp1 = " + post.timestamp.isoformat(timespec='seconds'))
      post.timestamp = post.timestamp.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
      pPosts2.append(post)
      # print("post.timestamp2 = " + post.timestamp.isoformat(timespec='seconds'))

    pLogs2=[]
    for plog in pLogs:
      log = copy.deepcopy(plog)
      # print("log.start1 = " + log.start.isoformat(timespec='seconds'))
      log.start = log.start.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
      # print("log.start2 = " + log.start.isoformat(timespec='seconds'))
      if log.stop:
        log.stop = log.stop.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
      pLogs2.append(log)

    # logs of other pilots who are active at the moment
    oLogs = PilotLog.query.filter(PilotLog.start >= date.today()).filter(PilotLog.stop == None).order_by(PilotLog.start.desc()) #.filter_by((PilotLog.start >= date.today())).order_by(PilotLog.start.desc())
    oLogs2 = []
    for olog in oLogs:
        # print("olog.start1 = " + olog.start.isoformat(timespec='seconds'))
        olog.start = olog.start.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
        # print("olog.start2 = " + olog.start.isoformat(timespec='seconds'))
        # print(olog.pilot.first_name)
        # print(olog.pilot.last_name+": "+str(olog.pilot.sichtbar))
        if olog.pilot.sichtbar:
            oLogs2.append(olog)


    posts = Post.query.filter(Post.timestamp >= date.today()).filter(Post.user_id != user.id)
    posts2 = []
    for post in posts:
        post.timestamp = post.timestamp.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
        posts2.append(post)

    # print("pPosts:")
    # print(type(pPosts))
    today = date.today().strftime('%Y-%m-%d')
    # print(today)
    form = EmptyForm()
    return render_template('pilot_index.html', user=user,
                           pLogs=pLogs2, oLogs=oLogs2,
                           pPosts=pPosts2,
                           posts=posts2,
                           todate=today,
                           form=form)


@bp.route('/dtpick')
def dtpick():
    # Test for timepicker
    form = MyDTPForm()
    tm = datetime.now()
    tm = tm - timedelta(minutes=tm.minute % 10,
                                 seconds=tm.second,
                                 microseconds=tm.microsecond)
    return render_template('tpTest.html', form=form, stime=tm)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/reportlist')
def reportlist():
    repDates = []
    from sqlalchemy import text
    sql = text("select  strftime('%Y-%m-%d', start) day, count(DISTINCT user_id) pilots from pilot_log group by strftime('%Y-%m-%d', start) order by 1 desc ;")
    result = db.engine.execute(sql)
    for r in result:
        repDates.append({"day": r.day, "pltanz": r.pilots})
        # print(r.day)
    return render_template('reportlist.html', days=repDates)

@bp.route('/report_md/<day>')
@bp.route('/report/<day>')
def report(day):
    # import copy
    if request.remote_addr != '127.0.0.1' and \
        (not current_user.is_authenticated or current_user.is_authenticated and current_user.ist_vorstand == None ):
        abort(403)  # Forbidden

    dayDate = datetime.strptime(day, '%Y-%m-%d')
    endday = sunset(dayDate)
    print("endday = " + endday.isoformat(timespec='seconds'))

    # Aufbereitung PilotenLogs
    pLogs = PilotLog.query.filter(PilotLog.start >= dayDate).filter(PilotLog.start <= endday)\
        .filter(PilotLog.flugleiter == 0).order_by(PilotLog.user_id, PilotLog.start ).all()
    pLogs2=[]
    for log in pLogs:
      # log = copy.deepcopy(plog)
      # print("log.start1 = " + log.start.isoformat(timespec='seconds'))
      log.start = log.start.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
      # print("log.start2 = " + log.start.isoformat(timespec='seconds'))
      if log.stop:
        log.stop = log.stop.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
      else:
          log.stop = tAbrund10(endday)
          print(log.stop)
          print(endday)
      if log.stop > log.start:
          pLogs2.append(log)

    # Aufbereitung FlugleiterLogs
    fLogs = PilotLog.query.filter(PilotLog.start >= dayDate).filter(PilotLog.start <= endday).\
      filter(PilotLog.flugleiter == 1).order_by(PilotLog.start ).all()
    fLogs2 = []
    for log in fLogs:
      log.start = log.start.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
      if log.stop:
        log.stop = log.stop.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
      else:
        log.stop = tAbrund10(endday)
      if log.stop > log.start:
        fLogs2.append(log)

      # log.username =
    form = EmptyForm()

    posts = Post.query.filter(Post.timestamp >= dayDate).filter(Post.timestamp <= endday)
    posts2 = []
    for post in posts:
        post.timestamp = post.timestamp.replace(tzinfo=gettz('UTC')).astimezone(gettz(current_app.config['LOC_TZ']))
        posts2.append(post)

    # print(pLogs2)
    # check which route was used to call this method
    srchRslt = re.search(r'^/report_md/', str(app.request.url_rule))
    if  srchRslt:
        return render_template('report_md.html', day=day,
                           pLogs=pLogs2,
                           fLogs=fLogs2,
                           pPosts=posts2,
                           # todate=today,
                           sunset=endday.strftime('%H:%M'),
                           form=form, mimetype='text/markdown')
    else:
        return render_template('report.html', day=day,
                               pLogs=pLogs2,
                               fLogs=fLogs2,
                               pPosts=posts2,
                               # todate=today,
                               sunset=endday.strftime('%H:%M'),
                               form=form, mimetype='text/markdown')


@bp.route('/user/<user_id>')
@login_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    # page = request.args.get('page', 1, type=int)
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.id)
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.sichtbar = form.sichtbar.data
        db.session.commit()
        flash(_('Die Änderungen wurden gespeichert.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        # form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.sichtbar.data = current_user.sichtbar

    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})



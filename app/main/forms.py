from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
from wtforms_components import read_only
from flask_babel import _, lazy_gettext as _l
from app.models import User

from datetime import date
from dateutil.tz import gettz

# from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
# from flask_wtf import Form
from wtforms.fields import DateField


class EditProfileForm(FlaskForm):
  #username = StringField(_l('Username'))
  first_name = StringField("Vorname")
  last_name =  StringField("Nachname")
  email = StringField("Email")
  about_me = TextAreaField(_l('Über mich'),
                           validators=[Length(min=0, max=140)])
  sichtbar = BooleanField("Deine Anmeldung soll für andere Kameraden sichtbar sein.", description='Deine Anmeldung ist für andere Kameraden sichtbar.')
  submit = SubmitField(_l('Speichern'))

  def __init__(self, id, *args, **kwargs):
    super(EditProfileForm, self).__init__(*args, **kwargs)
    self.id = id
    read_only(self.first_name)
    read_only(self.last_name)
    read_only(self.email)

  def validate_email(self, email):
    if email.data != self.email:
      user = User.query.filter_by(email=self.email.data).first()
      if user is not None:
        raise ValidationError(_('Please use a different email.'))


class EmptyForm(FlaskForm):
  submit = SubmitField('Abschicken')


class PilotIndex(FlaskForm):
  # date = DateField(id='datepick')
  today = date.today()

class PilotKommt(FlaskForm):
  # date = DateField(id='datepick')
  zeitKommt = StringField(id='datepick', label=_l('Zeit'),validators=[DataRequired(), Regexp('^[0-9]{2}:[0-9]{2}$')])
  flugleiter = BooleanField(_l('als Flugleiter'))
  submit = SubmitField(_l('Anmelden'))

class PilotGeht(FlaskForm):
  zeitGeht = StringField(id='datepick', label=_l('Zeit'),validators=[DataRequired(), Regexp('^[0-9]{2}:[0-9]{2}$')])
  submit = SubmitField(_l('Abmelden'))

class MyDTPForm(FlaskForm):
  date = DateField(id='datepick')
  flugleiter = BooleanField(_l('als Flugleiter'))
  submit = SubmitField(_l('Submit'))


class PostForm(FlaskForm):
  post = TextAreaField(_l('Meldung'), validators=[DataRequired()])
  submit = SubmitField(_l('Speichern'))


class SearchForm(FlaskForm):
  q = StringField(_l('Search'), validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    if 'formdata' not in kwargs:
      kwargs['formdata'] = request.args
    if 'meta' not in kwargs:
      kwargs['meta'] = {'csrf': False}
    super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
  message = TextAreaField(_l('Message'), validators=[
    DataRequired(), Length(min=1, max=140)])
  submit = SubmitField(_l('Speichern'))

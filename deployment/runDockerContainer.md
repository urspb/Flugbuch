# Erster Start

**Vorbemerkung:** Um die in diesem Abschnitt aufgeführten Befehle erfolgreich auszuführen, müssen diese im Wurzelverzeichnis des Projektes ausgeführt werden. Im Wurzelverzeichnis befindet sich u.a. die Datei `flugbuch.py`

## Erste Vorbereitungen
Voraussetzung für den Betrieb von Flugbuch ist eine funktionierende Python3-Installation (z.B. Python 3.8.10). Zudem müssen die Pakete installiert sein, die in der Datei `requirements.txt` aufgelistet sind. **Wer nicht weiß, wie das geht, sollte an dieser Stelle aufhören** und die Finger von _Flugbuch_ lassen.

## Weitere Vorbereitungen

Für den Start des Flugbuches wird eine Datenbank mit User-Einträgen benötigt. Im Repository ist eine Beispieldatenbank (`appExample.db`) mit vier Usern enthalten:

| first\_name | last\_name | email             | ist\_vorstand |
| :--- | :--- |:------------------|:-------------:|
| Duffy | Duck | d.duck@xyz.de     |               |
| Papa | Schlumpf | p.schlumpf@xyz.de |               |
| Mickey | Mouse | m.mouse@xyz.de    |       X       |
| John | Doe | j.doe@xyz.de      |               |

Das Passwort für alle User in dieser Datenbank ist `flugbuch`.

Mit dem Kommando 

    cp database/appExample.db database/app.db 
kann die Beispiel-Datenbank kopiert und für erste Tests verwendet werden. Wer eine leere Datenbank frisch aufbauen will, nutzt das Kommando:

    python -m flask db upgrade

Dann kann ein erster Test unternommen werden mit dem Befehl:

    python -m flask run

Unter der URL `http://127.0.0.1:5000/` kann dann ein erster Test von _Flugbuch_ erfolgen. Je nachdem ob der angemeldete Nutzer Vorstand ist, oder nicht, taucht der Menüpunkt _Berichte_ auf, oder eben nicht.

## Hinweis zur Datenbank
Die Email-Adressen in der Tabelle `USER` müssen klein geschrieben werden!

# _Flugbuch_ unter Docker
_Flugbuch_ kann in einem Docker-Container betrieben werden. Das hierfür notwendige Dockerfile ist im Wurzelverzeichnis zu finden.

## Build Docker Image
Um ein Dockerimage zu erzeugen, muss z.B. unter macOS dieser Befehl ausgeführt werden:

    sudo docker build -t flugbuch:latest .

## Run Docker container
Um das Docker-Image in einem Container zu starten, kann ein Befehl wie dieser genutzt werden:
```dockerfile
sudo docker run --name flugbuch -d -p 18000:15000 --rm \
    -e SECRET_KEY="secret-key-blablabla-end" \
    -e MAIL_SERVER=smtp.yourProvider.de -e MAIL_PORT=587 -e MAIL_USE_TLS=true \
    -e MAIL_USERNAME=<flugleiter.account@yourProvider.de> \
    -e MAIL_PASSWORD='<yourPWD>' \
    -v /z.b./var/services/FlugbuchContainer/database:/home/microblog/database \
    -v /z.b./var/services/FlugbuchContainer/logs:/home/microblog/logs \
    flugbuch:latest 
```
  

 

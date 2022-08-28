# The Fluchbuch!

The _Fluchbuch_ is a web app based on the example application by Miguel Gridberg featured in his [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). As the intended audience for this application is german, the rest of the documentation will be predominantly in german.

## Was ist Flugbuch?
_Flugbuch_...
* ist eine Web-Anwendung und erfordert daher funktionierenden Internetzugriff
* funktioniert auf allen (relevanten) Browsern, egal ob auf dem Desktop, Laptop, Tablet oder Smartphone
* ermöglicht es einem angemeldeten Benutzer seine eigenen Anwesenheiten auf dem Modellflugplatz zu erfassen mit folgenden Funktionen
  * Benutzer kommt (Auswahl Pilot / Flugleiter und Auswahl Uhrzeit)
  * Benutzer geht (Auswahl Uhrzeit)
  * Benutzer verfasst eine Meldung
* ist auf die wesentlichen Funktionen reduziert, die notwendig sind, um die in einer Aufstiegsgenehmigung enthaltene Pflicht zur Führung eines Flugbuches zu erfüllen
* sendet dem Benutzer auf Anforderung eine Email, wenn dieser sein Passwort vergessen hat, oder dieses aus anderen Gründen ändern möchte
* generiert Tagesberichte, mit allen Anwesenheitszeiten und Meldungen, die nur vom Vorstand eingesehen werden können
* speichert möglichst wenige Daten, um Konflikte mit der DSGVO zu vermeiden
* nutzt _SQLite_ als Datenbank-Engine um den Installations- und Wartungsaufwand möglichst gering zu halten.

## ... und was ist es nicht?
_Flugbuch_...
* ist keine eierlegende Wollmillchsau und wird es hoffentlich auch nie sein wollen
* sollte besser nicht von Menschen installiert, administriert und betrieben werden, die denken, sie wären IT-Experten, weil es ihnen schon einmal gelungen ist, ein Bild auf der Homepage ihres Vereins einzufügen.
* verfügt (derzeit) über keine Benutzerverwaltung, da sich nach dem Anlegen der Benutzer in der Regel nur äußerst selten etwas ändert. Änderungen der Benutzereinträge können sehr einfach direkt in der Datenbank vorgenommen werden, sofern man über die Kompetenz dafür verfügt ;-)

## Wie geht es weiter?
Eine kleine Anleitung zum Ausprobieren von Flugbuch findet sich [hier](deployment/runDockerContainer.md). Für alles, was darüber hinaus geht, ist (umfangreiches) eigenes Know-How erforderlich.

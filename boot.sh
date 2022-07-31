#!/bin/bash
# this script is used to boot a Docker container
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask translate compile
exec gunicorn -b 0.0.0.0:15000 --access-logfile - --error-logfile - flugbuch:app

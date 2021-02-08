#!/bin/sh
source venv/bin/activate
mkdir ./db
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - ecapi:app

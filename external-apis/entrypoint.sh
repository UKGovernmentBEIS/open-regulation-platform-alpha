#!/bin/sh

python src/orp_apps/manage.py migrate --no-input 
python src/orp_apps/manage.py collectstatic --no-input

uwsgi --http 0.0.0.0:80 --module orp_apps.wsgi

#!/usr/bin/env sh

BASEDIR=$(dirname $0)

set -e

echo "Running migrations..."
django-admin migrate --noinput

echo "Starting server..."
uwsgi --ini $BASEDIR/uwsgi.ini

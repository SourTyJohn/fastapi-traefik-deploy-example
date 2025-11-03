#!/bin/sh
python3 manage.py collectstatic --no-input

python3 manage.py migrate

python3 manage.py createsuperuser --no-input || true

exec gunicorn --bind 0.0.0.0:$WEB_PORT __settings__.wsgi

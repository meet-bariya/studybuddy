#!/bin/sh
SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-"meet@meetbariya.co"}
APP_PORT=${APP_PORT:-8000}

echo 'Running migrations...'
/opt/venv/bin/python manage.py migrate --noinput

echo 'Collecting static files...'
/opt/venv/bin/python manage.py collectstatic --no-input

echo 'Creating Superuser...'
/opt/venv/bin/python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm config.wsgi:application --bind "0.0.0.0:${APP_PORT}"
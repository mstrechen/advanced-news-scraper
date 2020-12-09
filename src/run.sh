#!/bin/bash

set -x

if [ "$MODE" == "WEB_PRODUCTION" ]; then
  KEYFILE=""
  CERTFILE=""
  EXTRA_PORT=""
  if [ -f "/certificates/privkey.pem" ]; then
    KEYFILE="--keyfile /certificates/privkey.pem";
    EXTRA_PORT="-b :443"
  fi
  if [ -f "/certificates/fullchain.pem" ]; then CERTFILE="--certfile /certificates/fullchain.pem"; fi
  # shellcheck disable=SC2086
  pipenv run gunicorn -w "${GUNICORN_WORKERS:-2}" -b :80 $EXTRA_PORT $CERTFILE $KEYFILE run:app
elif [ "$MODE" == "WEB" ]; then
    pipenv run python run.py
elif [ "$MODE" == "CELERY" ]; then
    pipenv run celery worker -A run:celery --loglevel=info -B --concurrency "${CELERY_CONCURRENCY:-2}" -Q "${CELERY_QUEUES:-celery}"
elif [ "$MODE" == "MIGRATE" ]; then
  export FLASK_APP=admin/app
  pipenv run flask db upgrade
elif [ "$MODE" == "DOWNGRADE" ]; then
  export FLASK_APP=admin/app
  pipenv run flask db downgrade
elif [ "$MODE" == "NEW_MIGRATION" ]; then
  export FLASK_APP=admin/app
  pipenv run flask db revision -m "$MIGRATION_MESSAGE"
elif [ "$MODE" == "GENERATE_TRANSLATIONS" ]; then
  cd admin || exit
  pipenv run pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
  pipenv run pybabel update -i translations/messages.pot -d translations
elif [ "$MODE" == "COMPILE_TRANSLATIONS" ]; then
  cd admin || exit
  pipenv run pybabel compile -d translations
elif [ "$MODE" == "TEST" ]; then
  export FLASK_APP=admin/app
  pipenv run pytest .
else
  echo "Unknown MODE=$MODE" && exit 1
fi

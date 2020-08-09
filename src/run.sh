#!/bin/bash

if [ "$MODE" == "WEB_PRODUCTION" ]; then
  pipenv run gunicorn -w "${GUNICORN_WORKERS:-2}" -b 0.0.0.0:80 run:app
elif [ "$MODE" == "WEB" ]; then
    pipenv run python run.py
elif [ "$MODE" == "MIGRATE" ]; then
  export FLASK_APP=admin/app
  pipenv run flask db upgrade
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
else
  echo "Unknown MODE=$MODE" && exit 1
fi

#!/bin/sh

# PostgreSQL Database settings
DB_NAME="refugee"
DB_PORT=5432
DB_HOST="localhost"
DB_USER=""
DB_PASSWORD=""

# Django Regulars
DJANGO_SETTINGS_MODULE="refugee_management.settings"
# PRODUCTION=true

# Shh! Secrets!!
SECRET_FILE="./.secret_key"
SECRET_LENGTH=32
# Create the secret file if it does not exist, otherwise NOP
[ -r $SECRET_FILE ] || < /dev/urandom LC_ALL=C tr -d -c "[:punct:][:alnum:]" | 2>/dev/null dd count=1 bs=$SECRET_LENGTH > $SECRET_FILE


# Call manage.py with the correct ENV variables


if [ "$PRODUCTION" = true ]
then
  export DB_NAME=$DB_NAME
  export DB_PORT=$DB_PORT
  export DB_HOST=$DB_HOST
  export DB_USER=$DB_USER
  export DB_PASSWORD=$DB_PASSWORD
  export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
  export PRODUCTION=$PRODUCTION
  export SECRET_KEY="$(cat $SECRET_FILE)"
  mkdir -p static
  if [ "$1" = "runserver" ]
  then
      python3 manage.py collectstatic --clear --noinput -v0
      nohup sh -c "uwsgi --ini uwsgi.ini" > /dev/null 2>&1 &
  else
      python3 manage.py $@
  fi
else
  DB_NAME=$DB_NAME \
  DB_PORT=$DB_PORT \
  DB_HOST=$DB_HOST \
  DB_USER=$DB_USER \
  DB_PASSWORD=$DB_PASSWORD \
  DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE \
  PRODUCTION=$PRODUCTION \
  SECRET_KEY="$(cat $SECRET_FILE)" \
  python manage.py $@
fi

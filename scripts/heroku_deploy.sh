#!/bin/sh -e
APP_NAME=$1

#git remote add heroku git@heroku.com:$APP_NAME.git
# git fetch heroku

MIGRATION_CHANGES=$(git diff HEAD heroku/master --name-only -- db | wc -l)
echo "$MIGRATION_CHANGES db changes."

PREV_WORKERS=$(heroku ps --app $APP_NAME | grep "^worker." | wc -l | tr -d ' ')

if test $MIGRATION_CHANGES -gt 0; then
  heroku maintenance:on --app $APP_NAME

  # Make sure workers are not running during a migration
  heroku scale worker=0 --app $APP_NAME

  heroku run python manage.py migrate --app $APP_NAME
  heroku scale worker=$PREV_WORKERS --app $APP_NAME
  heroku restart --app $APP_NAME

  heroku maintenance:off --app $APP_NAME

fi


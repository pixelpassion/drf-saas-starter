#!/bin/sh -e

APP_NAME=$1

git remote add heroku git@heroku.com:$APP_NAME.git

PREV_WORKERS=$(heroku ps --app $APP_NAME | grep "^worker." | wc -l | tr -d ' ')

# deploy code changes (and implicitly restart the app and any running workers)
git push heroku master -f

MIGRATION_CHANGES=$(heroku run python manage.py showmigrations | grep '\[ \]' | wc -l | tr -d ' ')
echo "$MIGRATION_CHANGES db changes since last deploy."

if test $MIGRATION_CHANGES -gt 0; then

  DEPLOY_START=`date +%s`

  heroku maintenance:on --app $APP_NAME

  # Make sure workers are not running during a migration

  if test $PREV_WORKERS -gt 0; then
    heroku scale worker=0 --app $APP_NAME
  fi

  heroku run python manage.py migrate --noinput --app $APP_NAME

  if test $PREV_WORKERS -gt 0; then
    heroku scale worker=$PREV_WORKERS --app $APP_NAME
  fi

  heroku run python manage.py clear_cache

  heroku restart --app $APP_NAME

  heroku maintenance:off --app $APP_NAME

  DEPLOY_END=`date +%s`
  ELAPSED=$(( $DEPLOY_END - $DEPLOY_START ))

  echo "Everything done. $ELAPSED seconds in maintenance mode."

fi

exit 0


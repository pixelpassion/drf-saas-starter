web: gunicorn main.wsgi:application
worker: celery worker --app=main.celery --loglevel=info

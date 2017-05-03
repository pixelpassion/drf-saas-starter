web: gunicorn main.wsgi:application
celery: celery worker --app=main.celery --loglevel=info
daphne: daphne main.asgi:channel_layer
runworker: python manage.py runworker -v2
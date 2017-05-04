web: daphne main.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
celery: celery worker --app=main.celery --loglevel=info
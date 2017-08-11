web: newrelic-admin run-program daphne main.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: newrelic-admin run-program python manage.py runworker -v2
celery: newrelic-admin run-program celery worker --app=main.celery --loglevel=info
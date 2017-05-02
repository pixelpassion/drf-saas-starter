web: gunicorn main.wsgi:application
celery: celery worker --app=main.celery --loglevel=info
daphne: python manage.py runworker -v2

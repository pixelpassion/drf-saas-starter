Docker
============

Local development
--------------------

### Download & install the Docker Community edition

* https://www.docker.com/community-edition


```
$ docker-compose build     # Build the containers (Django, Worker, Postgres DB, Redis, Mailhog)
$ docker-compose up        # Build the containers (Django, Worker, Postgres DB, Redis, Mailhog)

```

It will start different services locally.

* Django: http://localhost:8000
* Redis: rediscache://127.0.0.1:6379 (used for caching and django-channels)
* Redis Browser: http://localhost:8019/ (a simple Key/Value browser to debug Redis)
* Mailhog: http://localhost:8025 (a simple local mailserver for debugging mails)
* PostgreSQL database: postgres://postgres@localhost/einhorn_starter (can be used as a database, if set as a DATABASE_URL)
* RabbitMQ Management: http://localhost:15672/ (Management for RabbitMQ - for asynchronous tasks handling with Celery)






You can use the Docker shell to start manage.py commands:

```
$ docker-compose run django python manage.py migrate
$ docker-compose run django python manage.py createsuperuser
```




Production
--------------------

not used for now.



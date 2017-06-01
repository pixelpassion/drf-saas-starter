Docker
============

Local development
--------------------

Download & install the Docker Community edition:
* https://www.docker.com/community-edition

Build and start the containers::

    $ docker-compose build
    $ docker-compose up


It will start different services locally.

 * ``Django``: The webapplication itself (http://localhost:8000)
 * ``Documentation``: Automated Sphinx :doc:`documentation` (http://localhost:8007)
 * ``Mailhog``: A simple local mailserver for debugging mails, check out :doc:`email` (http://localhost:8025)
 * ``Postgres``: The used database, is used in ``DATABASE_URL`` (postgres:///einhorn-starter)
 * ``Redis``: Key-Value store for caching & :doc:`channels`, used as ``REDIS_URL`` (localhost:6379)
 * ``Redis Browser``: For debugging Redis key/values (http://localhost:8019/)
 * ``RabbitMQ Management``: For monitoring & debugging RabbitMQ, used for :doc:`celery` (http://localhost:15672)
 * A :doc:`channels` worker
 * A :doc:`celery` worker

It is possible to start single services (e.g. if you have your own Django setup and only need a particular service)::

    $ docker-compose up redis


Accessing containers
--------------------

For migrations run::

    $ docker-compose run django python manage.py migrate

For the creation of a superuser run::

    $ docker-compose run django python manage.py createsuperuser

You can access the Python shell::

    $ docker-compose run django python manage.py shell_plus


Also you can access the bash command line of the docker container::

    $ docker-compose run django bash

    (you need to type 'exit' to exit the bash) TODO?


Use in production
--------------------

The docker files can be used to be deployed into production. This is unsupported right now in favor of Heroku.


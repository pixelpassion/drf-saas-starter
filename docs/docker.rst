Docker
======

Local development
-----------------

You need to install Docker. Follow the instructions for your OS https://docs.docker.com/engine/installation/:

 - On Mac OS X: `Docker for Mac`_
 - On Windows: `Docker for Windows`_
 - On Linux: `docker-engine`_
.. _`Docker for Mac`: https://docs.docker.com/engine/installation/mac/
.. _`Docker for Windows`: https://docs.docker.com/engine/installation/windows/
.. _`docker-engine`: https://docs.docker.com/engine/installation/

Build and start the containers::

    $ docker-compose build
    $ docker-compose up


It will start different services locally.

 * ``Django``: The webapplication itself (http://localhost:8000), based on `Python 3.6 Slim <https://github.com/docker-library/python/blob/master/3.6/slim/Dockerfile>`_
 * ``Sphinx``: Automated Sphinx :doc:`documentation` with autobuild (http://localhost:8007)
 * ``Mailhog``: A simple local mailserver for debugging mails, check out :doc:`email` (http://localhost:8025)
 * ``Postgres``: The used database, is defined in ``DATABASE_URL`` (postgres:///einhorn-starter)
 * ``Redis``: Key-Value store for caching & :doc:`channels`, used as ``REDIS_URL`` (localhost:6379)
 * ``Redis Browser``: For debugging Redis key/values (http://localhost:8019)
 * ``RabbitMQ Management``: For monitoring & debugging RabbitMQ, used for :doc:`celery` (http://localhost:15672)
 * A :doc:`channels` worker
 * A :doc:`celery` worker

It is possible to start single services (e.g. if you have your own Django setup and only need a particular service)::

    $ docker-compose up redis


We are using Docker healthchecks:
 * Docker explanation: https://docs.docker.com/engine/reference/builder/#healthcheck
 * compose: https://docs.docker.com/compose/compose-file/#healthcheck
 * Example healthchecks: https://github.com/docker-library/healthcheck

For more information regarding Docker:
 * `Docker <https://docs.docker.com/get-started/>`_
 * `Docker compose <https://docs.docker.com/compose/overview/>`_



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
-----------------

The docker files can be used to be deployed into production. This is unsupported right now in favor of Heroku.


Deleting containers or images
-----------------------------

.. warning::
   You should only delete containers or images, when you know when you are doing.

Kill all running containers::

    docker kill $(docker ps -q)

Delete all stopped containers::

    docker rm $(docker ps -a -q)

Delete all images::

    docker rmi $(docker images -q)

Delete `dangling images <http://www.projectatomic.io/blog/2015/07/what-are-docker-none-none-images/>`_::

   docker rmi $(docker images -f "dangling=true" -q)

Fore more information:

* https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes


Postgres
--------

.. warning::
   The Port ``5432`` is not exposed to the outside, they will not interfer with any local Postgres databases. If you want to expose the ports, you need to add ``ports: "5432:5432"`` to the Postgres service in the ``docker-compose.yml``.

To access ``psql``, you need to get the ID of the Postgres container::

   $ docker ps -aqf name=postgres
   9b92a5a93aa5

Then you can start ``psql`` within the Container::

   docker exec -ti 9b9 psql -U postgres

Some useful commands::

   # Get all tables
   \dt
   # Get help for SQL commands
   \help
   # Exit
   \quit


Dry
---

``Dry <https://moncho.github.io/dry/>`` is a terminal application to manage and monitor Docker containers.

Installation ::

   $ curl -sSf https://moncho.github.io/dry/dryup.sh | sudo sh
   $ sudo chmod 755 /usr/local/bin/dry

Start it::

   $ dry

Press ``1`` to see the running containers, ``2`` for images and ``3`` for network informations.

You can check stats, see logs or restart a container etc.
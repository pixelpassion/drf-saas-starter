Testing
============

py.test
--------------------

We are using py.test for local tests::

    $ docker-compose run --rm django py.test

The ``--rm`` remove the container after run. If you get a message ``"test_postgres" can not be created`` or such it could be possible, that you have another container with the given command running.

Run only tests in one file::

    $ docker-compose run --rm django py.test apps/tenants/tests/test_api.py

Run tests of a specified class::

    $ docker-compose run --rm django py.test apps/tenants/tests/test_api.py::SignupApiTest

Run exactly one given test::

    $ docker-compose run --rm django py.test -k test_correct_signup_data


Tests
--------------------

Basics
~~~~~~~~

Channels
~~~~~~~~

We are using ``channels.test.ChannelTestCase`` base class - it swaps out the channel layer for a captive
in-memory layer, meaning we don't need an external server running to run tests.

Celery
~~~~~~~~

How to mock?

E-Mails / Sendgrid
~~~~~~~~

How to mock?

Coverage
--------------------

End to end
--------------------


CircleCI
--------------------

The circle.yml file..



Coverage
--------------------



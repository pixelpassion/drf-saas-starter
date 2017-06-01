Testing
============

py.test
--------------------

We are using py.test for local tests

Some useful commands:

```
$ pytest                                                            # Runs all tests
$ pytest apps/tenants/tests/test_api.py                             # Runs the tests in the file
$ pytest apps/tenants/tests/test_api.py::SignupApiTests             # Runs the tests of the specified class
$ pytest -k test_correct_signup_data                                # Runs the given test
```


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



# Onboarding

How to board an new developer

## Learning

### Learning Python

* Python Tutorial: https://docs.python.org/3/tutorial/
* Python Tutorial auf Deutsch: https://media.readthedocs.org/pdf/py-tutorial-de/python-3.3/py-tutorial-de.pdf

### Learning Django

* Django Documentation: https://docs.djangoproject.com/en/1.10/
* Django Tutorial: https://docs.djangoproject.com/en/1.10/intro/
* Two Scoops for Django: https://www.twoscoopspress.com/products/two-scoops-of-django-1-8
* Hello Web App: https://hellowebapp.com

## Github

## Slack

## Sentry

Errors are pushed to Sentry. Update the SENTRY_DSN setting in the .env

## Asynchronous tasks

Asynchronous tasks are used for taks, which really run asynchronous - for example bills, which are created in the background and then send to a user.

We are using Celery with RabbitMQ / CloudAMQP as a message broker.

## Websockets & django-channels

This is used for asynchronous, but more directly tasks - like messages to the user or an activity stream.

## Testing

We are using py.test for local tests

Some useful commands:

```
$ pytest                                                            # Runs all tests
$ pytest apps/tenants/tests/test_api.py                             # Runs the tests in the file
$ pytest apps/tenants/tests/test_api.py::SignupApiTests             # Runs the tests of the specified class
$ pytest -k test_correct_signup_data                                # Runs the given test
```

## Updating requirements

Add the requirement in base.in, local.in or production.in

```
fab pip             # Updates the base.txt, local.txt and production.txt files
fab pip:update      # Updates the requirements to the newest version (excluding the pinned ones)

pip install -r requirements/local.txt       # Install the changed pips locally
```


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

## Testing

We are using pytest for local tests

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
```


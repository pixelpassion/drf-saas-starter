Onboarding & Local development
============

New to Django?
--------------------

Check out these resources to learn Python and Django

* Python Tutorial: https://docs.python.org/3/tutorial/
* Python Tutorial auf Deutsch: https://media.readthedocs.org/pdf/py-tutorial-de/python-3.3/py-tutorial-de.pdf
* Django Documentation: https://docs.djangoproject.com/en/1.10/
* Django Tutorial: https://docs.djangoproject.com/en/1.10/intro/
* Two Scoops for Django: https://www.twoscoopspress.com/products/two-scoops-of-django-1-8
* Hello Web App: https://hellowebapp.com

Get started
--------------------

Did you read, how to :doc:`get_started` ?

Docker
--------------------

Please read the :doc:`docker` information next.

.env
--------------------

The project needs an .env file - it contains secret incredentials or such which should not be contained into the code.

A basic .env file is created automatically, when calling :doc:`./local_setup.py`:

The following entries are needed::

    DEBUG=True
    STAGE=local
    ALLOWED_HOSTS='*'
    DATABASE_URL=postgres:///einhorn-starter
    REDIS_URL=redis://127.0.0.1:6379
    SECRET_KEY='<a generated secret>'
    JWT_SECRET='<a generated secret>'

requirements
--------------------

We are using pip-compile for management of requirements.

If you want to add new requirements, you need to add them to base.in (the package is needed in development & production) or local.in (only locally needed) or production.in (only production use).

Run the following command afterwards to update the base.txt, local.txt and production.txt files::

    fab pip


Update requirements to the newest version, only excluding pinned packages::

    fab pip:update


Pycharm
--------------------

We recommend Pycharm for development. We included some files for easier onboarding. (TODO)

Testing
--------------------

Read more informations regarding :doc:`testing`.

Mailhog
--------------------

We are using Mailhog as a local mailserver in development. It receives mails at localhost:1025 and provides an mail client, served under https://localhost:8025/ (when using docker-compose).


Fabfile
--------------------

This package contains a fab file with some useful commands.

Cleaning and testing code::

    # Remove generated files like *.pyc etc.
    $ fab clean

    # Use flake8 to check Python style, PEP8 and McCabe complexity
    $ fab flake8

    # Automatically (re-)order of the import statements
    $ fab isort

    # Start tests
    $ fab test

    # Prepare code to be commited, it integrates clean, flake8, isort, test
    $ fab build

    # generate a coverage report
    $ fab coverage


Committing and pushing code::

    # Commit with a message
    $ fab commit:"My message"

    # Push commit
    $ fab push

    # Builds, Commit & push
    $ fab commit_and_push:"My message"


Pulling code::

    # Update the local environment (install requirement and migration)
    $ fab update

    # Pulls and updates the named branch, default is "master"
    $ fab pull_and_update
    $ fab pull_and_update:development


Deployment with Heroku::

    # Push to Heroku and makes migrations on the production database
    $ fab push_to_heroku

    # Create an heroku app
    $ fab create_heroku_app:name_of_cool_app

Other commands::

    # Get licenses of installed pip packaes, uses yolk
    $ fab licenses

    # Adding pip requirements (after adding packates to base.in, local.in or production.in)
    # fab pip

    # Updating pip requirements
    # fab pip:update

    # Create documentation
    # fab doc
    # fab doc:autobuild


Subdomains
------------------------------

To test and work with subdomains locally, you must change your ``/etc/hosts`` file::

    $ sudo nano /etc/hosts


Add the following line::

    127.0.0.1       a a.localhost


Restart domain services (OSX 10.9 and above)::

    $ sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder


Now ``a`` and ``a.localhost`` can be pinged or reached within any Browser.


What else
--------------------

You should get used to the concepts of :doc:`celery` and :doc:`channels`.



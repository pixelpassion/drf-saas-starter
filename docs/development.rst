Onboarding & Local development
==============================

New to Django?
--------------

Check out these resources to learn Python and Django

* Python Tutorial: https://docs.python.org/3/tutorial/
* Python Tutorial auf Deutsch: https://media.readthedocs.org/pdf/py-tutorial-de/python-3.3/py-tutorial-de.pdf
* Django Documentation: https://docs.djangoproject.com/en/1.10/
* Django Tutorial: https://docs.djangoproject.com/en/1.10/intro/
* Two Scoops for Django: https://www.twoscoopspress.com/products/two-scoops-of-django-1-11
* Hello Web App: https://hellowebapp.com

Get started
-----------

Did you read, how to :doc:`get_started`?

Docker
------

Please read the :doc:`docker` information next.

.env
----

The project needs an .env file - it contains secret credentials or such which should not be contained in the code.

A basic .env file is created automatically, when calling ``python local_setup.py``:

The following entries are needed::

    DEBUG=True
    STAGE=local
    ALLOWED_HOSTS='*'
    DATABASE_URL=postgres://postgres@postgres/postgres
    REDIS_URL=redis://redis:6379
    SECRET_KEY='<a generated secret>'
    JWT_SECRET='<a generated secret>'

requirements
------------

We are using pip-compile for management of requirements.

If you want to add new requirements, you need to add them to one of the ``.in``files, the `.txt` files are generated with the following command::

    make pip-compile

Update requirements to the newest version, only excluding pinned packages::

    make pip-update

There are different requirement files:

* base.txt (for packages needed in development & production)
* local.txt (only locally needed)
* production.txt (only production use)
* documentation.txt (for the Sphinx Docker container)

We are `saving hashes <https://pip.pypa.io/en/stable/reference/pip_install/#hash-checking-mode> `_ for more secure pip packages

Pycharm
-------

We recommend Pycharm for development. We included some files for easier onboarding. (TODO)

Testing
-------

Read more information regarding :doc:`testing`.

Mailhog
-------

We are using `Mailhog <https://github.com/mailhog/MailHog>`_ as a local mailserver in development. It receives mails at localhost:1025 and provides a mail client, served under `<http://localhost:8025>`_ (when using docker-compose).


Fabfile / Makefile
------------------

.. warning::
   We are moving from ``Fabric`` to ``make``. The following content is work in progress.

For a list of ``make`` commands, type in::

    $ make


For adding colors to a make command::

	@echo "\033[92mGreen!\033[0m"
	@echo "\x1b[33;01mYellow!\033[0m"
	@echo "\x1b[31;01mRed!\033[0m"


Cleaning and testing code::

    # Remove generated files like *.pyc etc.
    $ make clean

    # Use flake8 to check Python style, PEP8 and McCabe complexity
    $ fab flake8

    # Automatically (re-)order of the import statements
    $ fab isort

    # Start tests
    $ make test

    # Prepare code to be commited, it integrates clean, flake8, isort, test
    $ make build

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

    # Create a heroku app
    $ fab create_heroku_app:name_of_cool_app

Handling of requirements::

    # Get licenses of installed pip packaes, uses yolk
    $ fab licenses

    # Adding pip requirements (after adding packates to base.in, local.in or production.in)
    # make pip-compile

    # Updating pip requirements
    # make pip-update


Subdomains
----------

To test and work with subdomains locally, you must change your ``/etc/hosts`` file::

    $ sudo nano /etc/hosts


Add the following line::

    127.0.0.1       a a.localhost


Restart domain services (OSX 10.9 and above)::

    $ sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder


Now ``a`` and ``a.localhost`` can be pinged or reached within any Browser.


What else
---------

You should get used to the concepts of :doc:`celery` and :doc:`channels`.



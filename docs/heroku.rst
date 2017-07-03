Heroku
======

We are using the PaaS-Service Heroku for easier deployment.

Requirements
------------

Download and install the `Heroku CLI <https://devcenter.heroku.com/articles/heroku-command-line>`_.

If you haven't already, log into your Heroku account and follow the prompts to create a new SSH public key::

    $ heroku login

Create a new app using our Heroku setup script::

    $ fab create_heroku_app:cool-new-app

Using an existing Heroku app::

    $ heroku git:clone -a cool-new-app


Deployment
----------

Pushing to Heroku, either with Git or a Fabfile command::

    $ git push heroku master
    $ fab push_to_heroku

Checking the logs::

    $ heroku logs --app cool-new-app -f

Run commands or a shell::

    $ heroku run python manage.py shell --app cool-new-app
    $ heroku run python manage.py migrate --app cool-new-app


Procfile
--------

The Procfile lists the services / workers, which can be started on Heroku::

    web: daphne main.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
    worker: python manage.py runworker -v2
    celery: celery worker --app=main.celery --loglevel=info

Explanations:

* The web service is started automatically. We are using Daphne to support django-channels.
* The worker is part of django-channels.
* Celery is used for asynchronous tasks.


runtime.txt
-----------

The runtime names the Python version, used for deployment.

Heroku supports different versions (TODO: Link), django-saas-starter only works with Python 3.6+.


.slugignore
-----------

The project contains a ``.slugignore``. It contains a list of files in the repository, which are not needed for an Heroku deployment.

app.json
--------

The project contains an app.json file. It contains information how to deploy on Heroku. It is useful for automatic deployments of Git branches.

Domains & SSL
-------------

#### Setup domains and an SSL certificate:

Heroku takes care of SSL automatically for paid dynos. Check the `anncouncement <https://blog.heroku.com/announcing-automated-certificate-management>`_ or the `help page <https://devcenter.heroku.com/articles/automated-certificate-management>`_.

Enable certificates for an old app (it is automatically activated for old ones)::

    heroku certs:auto:enable -a cool-new-app

Add a domain::

    heroku domains:add test.yourdomain.de

Afterwards you have to set your DNS provider to the given domain.

You can check the status of domains & automated SSL handling::

    heroku domains
    heroku certs:auto

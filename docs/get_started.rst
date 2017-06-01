Get started
============

Concepts
--------------------

This template is used for Saas applications.

It is supposed to work for User-tenant-applications. The client can choose to register only one tenant (and all user registrations work for this one) or to add several tenants (adminstrators / billed partners of a platform), which can add users on their own.

Users

* need to be activated by the tenant.
* can edit their profile informations.
* can add comments to other users (or other objects in the system).
* can get notifications, when things happen (f.e. a comment is received)

The application is ready for business objects to be added to the system. Objects can have an activity stream (= a timeline) with actions regarding that object. The user itself has an activity stream as well (e.g. for comments).


Installation
--------------------

Install Docker as described in  :doc:`docker`

Clone the Github repository::

    $ git clone git@github.com/jensneuhaus/einhorn-starter

Start the local setup, it creates the required .env file::

    $ python local_setup.py

Start the Docker containers::

    $ docker-compose build
    $ docker-compose up

You should be able to open http://localhost:8000 in your browser.

.. warning::
   The following is work in progress. The installation procedere (Cookiecutter & PyPi) needs to be discussed.

Run the cookiecutter setup (TODO)

django-saas-starter is available on PyPI - to install it, just run::

    pip install -U django-saas-starter


It will install an package ``django-saas-starter`` and add it to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'django_saas_starter.users',
        'django_saas_starter.tenants',
        'django_saas_starter.mails',
        'django_saas_starter.comments',
        'django_saas_starter.activity_stream',
    )


That's it!

Now you can run :doc:`docker` for development or to run it locally. For deployment you should read :doc:`heroku`.



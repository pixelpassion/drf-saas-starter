Apps
============

django-saas-starter ships with some apps::


    INSTALLED_APPS = (
        ...
        'apps.users.apps.UsersConfig',
        'apps.tenants',
        'apps.mails',
        'apps.comments.apps.CommentsConfig',
        ...

    )



API
-----------------------------------------

The API app does not have models, so its not needed in INSTALLED_APPS.

The API provides functionality for the django-rest-framework integration:
* Feature 1
* Feature 2

User
-----------------------------------------

A customer user with some special features:

* Feature 1
* Feature 2

Fore more informations read :doc:`users`::


Tenants
-------


Handling for multi-tenancy. It takes care, that a user belongs to one or many tenants

settings in :doc:`settings.py`::
    TENANT_ROOT_SITE_ID=1      # What Site is used as a root domain for given subdomains?

Fore more informations read :doc:`users`::


Mails
-----------------------------------------

Handling of mails. It has some features:

* It uses django-anymail for sending with Sendgrid
* Saving mails to the database
* Use of dynamic mail templates

Fore more informations read :doc:`email`::


Comments
-----------------------------------------

The functionality to add comments to a given object, e.g. a user:

* Feature 1
* Feature 2

Activity stream
-----------------------------------------

A customer user with some special features:

* Feature 1
* Feature 2

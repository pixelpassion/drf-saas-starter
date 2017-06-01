Integrated apps
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

The API app does not have models, so its not included in INSTALLED_APPS.

The API provides functionality for the django-rest-framework integration:
* Sign in and Sign up for tenants and users.
* Password reset / forget endpoints
* Users listing / details with comments & activation-stream Endpoints
* A notification endpoint.

User
-----------------------------------------

A customer user with some special features:

* E-Mail required for sign up / sign in

Fore more informations read :doc:`users`:

Tenants
-------

Handling for multi-tenancy. It takes care, that a user belongs to one or many tenants.

* An registration for users within a tenant
* The possiblity for invites by a tenant
* Tenant Middleware for accessing tenant resources

Fore more informations read :doc:`users`:


Mails
-----------------------------------------

Handling of mails. It has some features:

* It uses django-anymail for sending with Sendgrid
* Saving mails to the database
* Use of dynamic mail templates

Fore more informations read :doc:`email`:


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

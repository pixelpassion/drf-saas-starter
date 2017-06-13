Integrated apps
===============

django-saas-starter ships with some apps.

User
----

A custom user with some special features:

* E-Mail required for sign up / sign in

Fore more information read :doc:`users`:

Tenants
-------

Handling for multi-tenancy. It takes care, that a user belongs to one or many tenants.

* A registration for users within a tenant
* The possiblity for invites by a tenant
* Tenant Middleware for accessing tenant resources

For more information read :doc:`users`:


Mails
-----

Handling of mails. It has some features:

* It uses django-anymail for sending with Sendgrid
* Saving mails to the database
* Use of dynamic mail templates

Fore more information read :doc:`email`:


Comments
--------

The functionality to add comments to a given object, e.g. a user:

* Feature 1
* Feature 2

Activity stream
---------------

A custom user with some special features:

* Feature 1
* Feature 2

API
============

We are using django-rest-framework to provide an API.

The API provides functionality for the django-rest-framework integration:
* Sign in and Sign up for tenants and users.
* Password reset / forget endpoints
* Users listing / details with comments & activation-stream Endpoints
* A notification endpoint.

Authentication
--------------------

django-rest-auth and django-allauth are used to provide authentication.

We are using JWT (link to specification) with following user informations provided after a sign in::

Endpoints
--------------------

More infos within Swagger.

current_user
~~~~~~~~

login
~~~~~~~~

logout
~~~~~~~~

password
~~~~~~~~

sign_up
~~~~~~~~

users
~~~~~~~~

with comments



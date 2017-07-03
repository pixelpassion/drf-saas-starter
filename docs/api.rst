API
===

We are using django-rest-framework to provide an API.

The API provides functionality for the django-rest-framework integration:

* Sign in and Sign up for tenants and users.
* Password reset / forget endpoints.
* Users listing / details with comments & activation-stream Endpoints.
* A notification endpoint.

Authentication
--------------

django-rest-auth and django-allauth are used to provide authentication::

We are using `JWT <https://jwt.io>`_ (`RFC7159 <https://tools.ietf.org/html/rfc7519>`_).

After successful login, a JWT token is sent back to the client. The token needs to be saved in the client.



For protected endpoints an HTTP Authentication header needs to be sent from the client::

    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....


Pagination
----------

You can use the ``page`` parameter in the URL to paginate a list of results. The size of the page can be set with ``page_size`` parameter.

Request::

    GET /api/users/?page=2&page_size=50

Response::

    HTTP 200 OK
    {
        "count": 1023
        "next": "api/users/?page=3",
        "previous": "api/users/?page=2",
        "results": [
           …
        ]
    }

HTTP Status codes
-----------------

Everything is okay:

* 200 - `OK`
* 201 - `Created something`
* 304 - `Not modified`

An error happened:

* 400 - Bad Request (the user did something wrong probably)
* 401 - Unauthorized (the Authorization seems not valid)
* 403 - Forbidden (User authorized, but one particular action is forbidden)
* 405 - Method Not Allowed (Used a not allowed method for that endpoint)
* 500 - Internal Server error (API Backend problem)



Endpoints
---------

You find some basic information here, more info within Swagger.

current_user
~~~~~~~~~~~~

login
~~~~~

The following information is sent after a successful sign in::

    {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
      "user": {
        "pk": "12345678-1234-abcd-1234-123456789abc",
        "username": "john",
        "email": "john.doe@gmail.com",
        "first_name": "John",
        "last_name": "Doe"
      }
    }

logout
~~~~~~

password
~~~~~~~~

sign_up
~~~~~~~

users
~~~~~

with comments

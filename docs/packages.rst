Used packages
=============


Django (MIT Licence)
--------------------

* `Django <https://github.com/django/django>`_: Django framework itself (`License <https://www.djangoproject.com>`_, `Documentation <https://docs.djangoproject.com/en/1.10/>`_)


django-environ
--------------

* `django-environ <https://github.com/joke2k/django-environ>`_: Configuration by environment variables according to 12Factor model (`License <https://github.com/joke2k/django-environ/blob/develop/LICENSE.txt>`_, `Documentation <https://django-environ.readthedocs.io>`_)


django-allauth
--------------

* `django-allauth <https://github.com/pennersr/django-allauth/>`_: For user registration, either via email or Open ID Providers (`License <https://github.com/pennersr/django-allauth/blob/master/LICENSE>`_, `Documentation <https://django-allauth.readthedocs.io/en/latest/>`_)


django-rest-framework
---------------------

* `djangorestframework <https://github.com/tomchristie/django-rest-framework>`_: RESTful API Handling (`License <https://github.com/tomchristie/django-rest-framework/blob/master/LICENSE.md>`_, `Documentation <http://www.django-rest-framework.org>`_)
* `django-rest-swagger <https://github.com/marcgibbons/django-rest-swagger>`_: (`License <https://github.com/marcgibbons/django-rest-swagger/blob/master/LICENSE>`_, `Documentation <http://marcgibbons.github.io/django-rest-swagger/>`_)
* django-cors-headers         # Adds CORS (Cross-Origin Resource Sharing) headers to responses
* django-rest-auth            # Authentication with the django-rest-framework
* djangorestframework-jwt     # JSON Web token support


django-anymail
--------------

* `django-anymail <https://github.com/anymail/django-anymail>`_: Email handling (`License <https://github.com/anymail/django-anymail/blob/master/LICENSE>`_, `Documentation <https://anymail.readthedocs.io/en/stable/>`_)

* `sendgrid <https://github.com/sendgrid/sendgrid-python/>`_: (`License <https://github.com/sendgrid/sendgrid-python/blob/master/LICENSE.txt>`_, `Documentation <https://github.com/sendgrid/sendgrid-python/blob/master/USAGE.md>`_)
* sendgrid                    # just for testing, we should use django-anymail to be more flexible


channels
--------

* channels
* django-channels-panel
* Twisted[tls,http2]          # Twisted with TLS & https2 support
* asgi-redis


django-activity-stream
----------------------


django-nyt
----------

* Notification system (needs to be pinned because --pre is not working)


Others
------

* `psycopg2 <https://github.com/psycopg/psycopg2>`_: PostgreSQL Database connector (`License <https://github.com/psycopg/psycopg2/blob/master/LICENSE>`_), `Documentation <http://pythonhosted.org/psycopg2/>`_)
* raven, for Sentry Error handling
* django-extensions           # Django extensions (should be in local.txt after done with testing)
* argon2-cffi                 # password hashing
* django-redis                # Redis handling
* django-tinymce              # HTMLField for models
* html2text                   # Convert HTML to Markdown

* `whitenoise <https://github.com/evansd/whitenoise>`_: Static file serving (`License <https://github.com/evansd/whitenoise/blob/master/LICENSE>`_, `Documentation <http://whitenoise.evans.io/en/stable/>`_)
* `django-rosetta <https://github.com/mbi/django-rosetta>`_: (`License <https://github.com/mbi/django-rosetta/blob/develop/LICENSE>`_), `Documentation <http://django-rosetta.readthedocs.io/en/latest/>`_)


Requirements of requirements
----------------------------

For a complete list of all used packages check out the ``requirements/local.txt`` and ``requirements/production.txt``.
Thanks to pip-compile these files are containing all installed packages. This means it contains the required packages of required packages and so on.


Old list
--------


* `django-localflavor <https://github.com/django/django-localflavor>`_: (`License <https://github.com/django/django-localflavor/blob/master/LICENSE>`_), `Documentation <https://django-localflavor.readthedocs.io/en/latest/>`_)
* django-premailer            # Inline CSS in HTML email templates

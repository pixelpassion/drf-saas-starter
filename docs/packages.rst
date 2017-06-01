Used packages
============


Django (MIT Licence)
--------------------

* [Django](https://github.com/django/django): Django framework itself ([License](https://www.djangoproject.com), [Documentation](https://docs.djangoproject.com/en/1.10/))

django-environ
--------------------

* [django-environ](https://github.com/joke2k/django-environ): Configuration by environment variables according to 12Factor model ([License](https://github.com/joke2k/django-environ/blob/develop/LICENSE.txt), [Documentation](https://django-environ.readthedocs.io))

Configuration by environment variables according to 12Factor model

django-allauth
--------------------

* [django-allauth](): For user registration, either via email or Open ID Providers ([License](), [Documentation]())



django-rest-framework
--------------------

* [djangorestframework](https://github.com/tomchristie/django-rest-framework): RESTful API Handling ([License](https://github.com/tomchristie/django-rest-framework/blob/master/LICENSE.md), [Documentation](http://www.django-rest-framework.org))
* [django-rest-swagger](https://github.com/marcgibbons/django-rest-swagger): ([License](https://github.com/marcgibbons/django-rest-swagger/blob/master/LICENSE), [Documentation]())
* django-cors-headers         # Adds CORS (Cross-Origin Resource Sharing) headers to responses
* django-rest-auth            # Authentication with the django-rest-framework
* djangorestframework-jwt     # JSON Web token support


django-anymail
--------------------

* [django-anymail](): Email handling ([License](), [Documentation]())

* [sendgrid](): ([License](), [Documentation]())
* sendgrid                    # just for testing, we should use django-anymail to be more flexible



channels
--------------------


* channels
* django-channels-panel
* Twisted[tls,http2]          # Twisted with TLS & https2 support
* asgi-redis


django-activity-stream
----------------------


django-nyt
----------------------

* Notification system (needs to be pinned because --pre is not working)


Others
--------------------

* [psycopg2](https://github.com/psycopg/psycopg2): PostgreSQL Database connector ([License](https://github.com/psycopg/psycopg2/blob/master/LICENSE), [Documentation](http://pythonhosted.org/psycopg2/))
* raven, for Sentry Error handling
* django-extensions           # Django extensions (should be in local.txt after done with testing)
* argon2-cffi                 # password hashing
* django-redis                # Redis handling
* django-tinymce              # HTMLField for models
* html2text                   # Convert HTML to Markdown

* [whitenoise](): Static file serving ([License](), [Documentation]())
* [django-rosetta](https://github.com/mbi/django-rosetta): ([License](https://github.com/mbi/django-rosetta/blob/develop/LICENSE), [Documentation](http://django-rosetta.readthedocs.io/en/latest/))


Requirements of requirements
--------------------

For a complete list of all used packages check out the ``requirements/local.txt`` and ``requirements/production.txt``.
Thanks to pip-compile these files are containing all installed packages. This means it contains the required packages of required packages and so on.


Old list
--------------------


* [django-localflavor](https://github.com/django/django-localflavor): ([License](https://github.com/django/django-localflavor/blob/master/LICENSE), [Documentation](https://django-localflavor.readthedocs.io/en/latest/))
* django-premailer            # Inline CSS in HTML email templates

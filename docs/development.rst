Onboarding & Local development
============

New to Django?
--------------------

Check out these resources to learn Python and Django

* Python Tutorial: https://docs.python.org/3/tutorial/
* Python Tutorial auf Deutsch: https://media.readthedocs.org/pdf/py-tutorial-de/python-3.3/py-tutorial-de.pdf
* Django Documentation: https://docs.djangoproject.com/en/1.10/
* Django Tutorial: https://docs.djangoproject.com/en/1.10/intro/
* Two Scoops for Django: https://www.twoscoopspress.com/products/two-scoops-of-django-1-8
* Hello Web App: https://hellowebapp.com

Docker
--------------------

Please read the Docker page.


.env
--------------------

The project needs an .env file - it contains secret incredentials or such which should not be contained into the code.

requirements
--------------------

We are using pip-compile for management of requirements.

Add a new requirement
~~~~~~~~

Add the requirement to base.in, local.in or production.in.

```
fab pip             # Updates the base.txt, local.txt and production.txt files
```

Update requirements
~~~~~~~~

```
fab pip:update      # Updates the requirements to the newest version (excluding the pinned ones)
```

You can pin packages, if some versions are not compatible.

Pycharm
--------------------

We recommend Pycharm for development. We included some files for easier onboarding. (TODO)


Testing
--------------------

Read the testing file.


Fabfile
--------------------

This package contains a fab file with some useful commands


What else


You should get used to the concepts of :doc:`celery`: and :doc:`channels`:

Handling of subdomains locally
------------------------------

To try subdomains, you can locally change your /etc/hosts file:

```
$ sudo nano /etc/hosts
```

Add the following line:
```
127.0.0.1       a a.localhost b.localhost c.localhost d.localhost
```

Restart domain services (OSX 10.9 and above)

```
$ sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

Now `a` and `a.localhost` etc. can be pinged or reached within any Browser.



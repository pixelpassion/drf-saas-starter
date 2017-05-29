[![einhornmanufaktur](https://img.shields.io/badge/made%20by-einhornmanufaktur-blue.svg)](https://www.einhornmanufaktur.de/)
[![Build Status](https://circleci.com/gh/jensneuhaus/einhorn-starter.png?style=shield&circle-token=36515d7bdb2ff036a488c3b58bea07e80bf2fad1)](https://circleci.com/gh/jensneuhaus/einhorn-starter/)

## Basic idea

* Helps a project kickoff with ALWAYS needed services (asynchronous tasks, Websockets, mail sending, cache, error handling etc.)
* The added apps are pretty modular and can be turned on / off or configured on the fly
* Requirements: Uses Django 1.10.x and Python 3.6.x

## Features

* Optimized for Python 3.6+ and Django 1.10+
* [12-Factor](12factor.net) based settings via [django-environ](12factor.net)
* Based on an API build with the awesome [django-rest-framework](#)
* API documentation build with [Swagger](#)
* Optimized testing with [py.test](https://docs.pytest.org/en/latest/) & coverage of > 90%
* [Fabric](#) for faster and easier deployments
* Send emails via [Anymail](#) (using [Sendgrid](#) as default)
* Serving dynamic HTML E-Mail Templates, editable with [Tinymce](#)
* [Docker-compose](#) File for easier development
* Support for Channels with [django-channels](#), optimized for [Heroku](https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django)
* Build in support for [Sentry](#) Error monitoring
* Deployment for Heroku with [Procfile](#), [app.json](#), [Whitenoise](#)
* Custom user, multi-tenancy and feature-Handling with [django-waffle](#)
* Continuous integration with [CircleCI](#)

## Local setup

### Download & install the Docker Community edition

* https://www.docker.com/community-edition


```
$ docker-compose build     # Build the containers (Django, Worker, Postgres DB, Redis, Mailhog)
$ docker-compose up        # Build the containers (Django, Worker, Postgres DB, Redis, Mailhog)

```

It will start different services locally.

* Django: http://localhost:8000
* Redis: rediscache://127.0.0.1:6379 (used for caching and django-channels)
* Redis Browser: http://localhost:8019/ (a simple Key/Value browser to debug Redis)
* Mailhog: http://localhost:8025 (a simple local mailserver for debugging mails)
* PostgreSQL database: postgres://postgres@localhost/einhorn_starter (can be used as a database, if set as a DATABASE_URL)
* RabbitMQ Management: http://localhost:15672/ (Management for RabbitMQ - for asynchronous tasks handling with Celery)

You can use the Docker shell to start manage.py commands:

```
$ docker-compose run django python manage.py migrate
$ docker-compose run django python manage.py createsuperuser
```

### Handling of subdomains locally

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

## Deployment to Heroku

### Creating an new Heroku app

#### Heroku Setup

Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line)

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```
$ heroku login
```

#### Create a new app

Use our Heroku setup script:

```
$ fab create_heroku_app:cool-new-app
```

#### Setup domains and an SSL certificate:

Heroku takes care of SSL automatically for paid dynos. Check the [anncouncement](https://blog.heroku.com/announcing-automated-certificate-management) or the [help page](https://devcenter.heroku.com/articles/automated-certificate-management).


```
heroku certs:auto:enable -a cool-new-app                    # Only needed for already existing apps
heroku domains:add test.yourdomain.de                       # Add an domain, set the DNS to the given domain

heroku domains                                              # Checks all domains
heroku certs:auto                                           # Checks the status of the automated SSL handling
```


### Using an existing Heroku app

```
$ heroku git:clone -a cool-new-app
```

### Working with Heroku

Pushing to Heroku:

```
$ git push heroku master

or

$ fab push_to_heroku
```

Checking the logs

```
$ heroku logs --app cool-new-app -f
```

Run commands or a shell

```
heroku run python manage.py shell --app cool-new-app
heroku run python manage.py migrate --app cool-new-app
```


## Contributing?

Are you contributing to the project? You can read more in [Onboarding as a new developer](docs/onboarding.md)

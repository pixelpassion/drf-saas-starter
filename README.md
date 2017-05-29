[![einhornmanufaktur](https://img.shields.io/badge/made%20by-einhornmanufaktur-blue.svg)](https://www.einhornmanufaktur.de/)
[![Build Status](https://circleci.com/gh/jensneuhaus/einhorn-starter.png?style=shield&circle-token=36515d7bdb2ff036a488c3b58bea07e80bf2fad1)](https://circleci.com/gh/jensneuhaus/einhorn-starter/)

## Basic idea

* Helps a project kickoff with ALWAYS needed services (asynchronous tasks, Websockets, mail sending, cache, error handling etc.)
* The added apps are pretty modular and can be turned on / off or configured on the fly
* Requirements: Uses Django 1.10.x and Python 3.6.x

## Features

* Optimized for Python 3.5+ and Django 1.10
* [12-Factor](12factor.net) based settings via [django-environ](12factor.net)
* HTML Generator build in with [weasyprint](#)
* Based on an API build with the awesome [django-rest-framework](#)
* API documentation build with [Swagger](#)
* Testing with [py.test](#)
* Fabric for faster deployments
* Send emails via [Anymail](#) (using [Sendgrid](#) as default)
* HTML Templates with Tinymce
* Dockerfile for development
* Support for Channels with [django-channels](#), optimized for [Heroku](https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django)
* Optimized for speed
* Script for developer onboarding
* Build in support for [Sentry](#)
* Deployment for Heroku with [Procfile](#) and [Whitenoise](#)
* --Tested with coverage of 100%--
* Custom user, Multitenancy and Feature-Handling
* Continuous integration with [CircleCI](#)

## Local setup

```
$ ./local_setup {{project_name}}        # Will create a database, a virtual environment folder .venv and an .env file
$ source .venv/bin/activate             # Start the virtual environment
$ pip install fabric3                   # Installs fabric3
$ fab update                            # Updates requirements and migrations etc.
```

## Docker

Download & install Docker Community Edition

* https://www.docker.com/community-edition

Start all the services (they will be built once)

```
$ docker-compose -f dev.yml up
```

It will start different services locally.

* RabbitMQ Management: http://localhost:15672/ (Management for RabbitMQ - for asynchronous tasks handling)
* Redis: rediscache://127.0.0.1:6379 (used for caching and django-channels)
* Redis Browser: http://localhost:8019/ (a simple Key/Value browser to debug Redis)
* Mailhog: http://localhost:8025 (a simple local mailserver for debugging mails)
* PostgreSQL database: postgres://postgres@localhost/einhorn_starter (can be used as a database, if set as a DATABASE_URL)

## Onboarding

Are you contributing to the project? You can read more in [Onboarding as a new developer](docs/onboarding.md)

## Setup as a new Project

You want to start a new project? Read more about the [Individual Project Setup](docs/project_setup.md)

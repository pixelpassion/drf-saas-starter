[![unicorn.supplies](https://img.shields.io/badge/made%20by-unicorn.supplies-blue.svg)](https://www.unicorn.supplies/)
[![Build Status](https://circleci.com/gh/jensneuhaus/einhorn-starter.png?style=shield&circle-token=36515d7bdb2ff036a488c3b58bea07e80bf2fad1)](https://circleci.com/gh/jensneuhaus/einhorn-starter/)

# `drf-saas-starter`

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

## Documentation

Read our documentation at ..

## Local setup

Download & install the Docker Community edition
* https://www.docker.com/community-edition

Run the following commands, it will build & start the needed containers (Django, Worker, Postgres DB, Redis, Mailhog)*[]:

```
$ docker-compose build
$ docker-compose up
```

Open your browser and go to http://localhost:8000/

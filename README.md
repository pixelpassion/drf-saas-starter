[![einhornmanufaktur](https://img.shields.io/badge/made%20by-einhornmanufaktur-blue.svg)](https://www.einhornmanufaktur.de/)
[![Build Status](https://circleci.com/gh/jensneuhaus/einhorn-starter.png?style=shield&circle-token=36515d7bdb2ff036a488c3b58bea07e80bf2fad1)](https://circleci.com/gh/jensneuhaus/einhorn-starter/)

## Features

* Optimized for Python 3.5+ and Django 1.10
* [12-Factor](12factor.net) based settings via [django-environ](12factor.net)
* SSL Support with [letsencrypt](#)
* HTML Generator build in with [weasyprint](#)
* Based on an API build with the awesome [django-rest-framework](#)
* API documentation build with [Swagger](#)
* Fabric for faster deployments
* Send emails via [Anymail](#) (using [Sendgrid](#) as default)
* HTML Templates with Tinymce
* Dockerfile for development
* Support for Channels with [django-channels](#)
* Optimized for speed
* Script for developer onboarding
* Build in support for [Sentry](#)
* Deployment for Heroku with [Procfile](#) and [Whitenoise](#)
* --Tested with coverage of 100%--
* Custom user, Multitenancy and Feature-Handling
* Continuous integration with [CircleCI](#)

# Template

* Helps a project kickoff with ALWAYS needed services (asynchronous tasks, Websockets, mail sending, cache, error handling etc.)
* The added apps are pretty modular and can be turned on / off or configured on the fly
* Uses Django 1.10.x and Python 3.5.2
* [Individual Project Setup](docs/project_setup.md)
* [Roadmap](docs/roadmap.md)

## Local setup

```
$ ./local_setup {{project_name}}        # Will create a database and an virtual environment folder .venv
$ source .venv/bin/activate             # Start the virtual environment
$ pip install fabric3                   # Installs fabric3
$ fab update                            # Updates requirements and migrations etc.
$ npm install                           # Installing frontend packages
```

## Administration

* https://einhorn-starter.herokuapp.com/admin/ (admin / test1234)

## Static files

Install node.js, npm, gulp etc.:

    $ npm install
    $ npm run watch


## Heroku

Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line)

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```
$ heroku login
```

For existing repositories, simply add the heroku remote

```
$ heroku git:remote -a einhorn-starter
```

Push to heroku

```
$ git push heroku master

or

$ fab push_to_heroku
```

Check the logs

```
$ heroku logs --app einhorn-starter -f                                                                                                                                              
```

Run commands or a shell

```
heroku run "python manage.py shell" --app einhorn-starter
```

## Environments

Start ./local_setup.py to generate an .env and edit missing configs to get everything working.

## Sentry

* Errors are pushed to Sentry. Update the SENTRY_DSN setting in the .env

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

## Asynchronous tasks

Asynchronous tasks are used for taks, which really run asynchronous - for example bills, which are created in the background and then send to a user.

We are using RabbitMQ / CloudAMQP as a message broker and Nameko for prodiving the services.

## Websockets & django-channels

This is used for asynchronous, but more directly tasks - like messages to the user or an activity stream. 

## Subdomains

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

## SSL (letsencrypt)

```
sudo certbot certonly --manual

heroku config:set ACME_TOKEN=
heroku config:set ACME_KEY=

sudo heroku certs:add /etc/letsencrypt/live/starter.einhornmanufaktur.de/fullchain.pem /etc/letsencrypt/live/starter.einhornmanufaktur.de/privkey.pem --app einhorn-starter

heroku config:set SECURE_SSL_REDIRECT=True

```

# einhorn-starter

* Helps to get a Einhornmanufaktur project started

## Local setup

```
$ ./local_setup {{project_name}}        # Will create a database and an virtual environment folder .venv
$ source .venv/bin/activate             # Start the virtual environment
$ pip install fabric3                   # Installs fabric3
$ fab update                            # Updates requirements etc.
```



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
```

## Environments

Copy the .env.example to .env and edit the missing configs to get everything working

## Sentry

* Errors are pushed to Sentry. Update the SENTRY_DSN setting in the .env

## Docker

* (will be added later)

## Celery

Install the RabbitMQ Management Docker file 

Start the worker

```
$ ...
```

# Old stuff

## Strategic Basics

* I have several ideas and we need a template, we can use as a base instead of doing over and over again
* Things I would build out of it:
 * A product page to advertise + test ideas. A onepage landingpage with an introduction, a form, a newsletter signup, A/B-testing and Adwords + FB ads integration
 * The market place for products and companies with profile pages for each product and the possibility to order or buy things - with statistics and logins for either stakeholder.
 * ...

## Technical basics

* newest Django 1.10.x, Python 3.x
* all apps should be seperated logically, so that they could run stand alone or the rest would still work
* please have all tested correctly

## Should be deployable on Heroku

* Check modern-webpages for that
* Use whitenoise
* On https://dashboard.heroku.com/apps/einhorn-default
* Maybe we integrate Digital Ocean as a fallback as well

## django-environ for environment variables & one settings file & .env

* Check modern-webpages for that

## Install Sentry + test error logging

* https://sentry.io/einhornmanufaktur/django-starter/getting-started/python-django/
* SENTRY_DSN='https://d8149058f0924193aa9af8a87e8dca83:fec43582f54b4c448882b44a7ce308a3@sentry.io/122593'

## Docker compose

* It should be easy to get a local Docker image for RabbitMQ and Mailhog, I can help you with that
* We can orientate on cookiecutter django for that or https://github.com/realpython/dockerizing-django

## Asynchronous server

* Use Celery + CloudAmq on Heroku

## letsencrypt SSL

* Checkout cookiecutter!

## Mail sending with django-anymail & Mailgun

* Install django-anymail and make it possible to have asynchronous email
* Mailgun credentials: https://dashboard.heroku.com/apps/einhorn-default/settings
* Mail needs to be sent asynchronous
* Build 

## Static files handling

* node, grunt or gulp for static file handling - lets discuss

## Install django-rest-framework

* We need a separated backend + frontend
* We need an API for Signup, Signin user type A, signin user type B, Passwort change and passwort recovery

## Registration + Passwort forget

* Either django-allauth or django-registration(-redux), await instructions please, maybe we do not need it because of the APis

## React + HTML5 Boilerplate + Bootstrap 4.0

* Fully seperated and a new Django App
* Install React as a seperated app with no models and views
* It should communicate with the API (Signin, Signup, Passwort forget, etc.)
* Check HTML5 Boilerplate Webpage (if needed with Redux?)
* Setup Django Flatpages for the setup of pages in the Admin (checkout modern webpages)
* Static pages: Startpage, Imprint 
* Integration from a cool template we buy or make

## Integrate django-channels

* Have a live test, where you send something to the server and it gets reloaded in the other one (for example automatically logout, when you logout on another browser)
* https://channels.readthedocs.io/en/stable/

## A nice form integration

* django-crispy-forms? Something from React, just using a form API?
* Renders API posts as forms or rather vice versa - can send beautiful forms to an API and prints errors very good.
* Is being able to have form wizards

## Setup Jenkins

* Setup a Jenkins Docker container on Digital ocean
* Integrate Jenkins
* Write API tests for the django-rest-framework APIs

# For later

## Statistics

* Which page was viewed from whom? Where did the user come from?

## django-waffle should be installed as a feature switch

* tbd

## Google Adwords API

* tbd

## Facebook Ads API

* tbd

## PDF generation with XHTML

* tbd

## A/B-Testing

* tbd 

##  Activity stream

* tbd

## Messaging stream


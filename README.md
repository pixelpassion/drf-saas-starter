# Einhornmanufaktur Boilerplate

* Helps a project kickoff with ALWAYS needed services (asynchronous tasks, Websockets, mail sending, cache, error handling etc.)
* The added apps are pretty modular and can be turned on / off or configured on the fly
* Uses Django 1.10.x and Python 3.5.2
* About an individual [project setup guide](docs/project_setup.md)

## Local setup

```
$ ./local_setup {{project_name}}        # Will create a database and an virtual environment folder .venv
$ source .venv/bin/activate             # Start the virtual environment
$ pip install fabric3                   # Installs fabric3
$ fab update                            # Updates requirements and migrations etc.
```

## Administration

* https://einhorn-starter.herokuapp.com/admin/ (admin / test1234)

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

Install Docker and make it accessible in the Terminal:

* https://docs.docker.com/docker-for-mac/ OR https://kitematic.com

```
$ eval $(docker-machine env)
```

Start Docker

```
$ fab docker
```

It will start different services locally.

* RabbitMQ Management: http://192.168.99.100:15672/
* Mailhog Mailserver: http://192.168.99.100:8025
* PostgreSQL: To use it, set DATABASE_URL=postgres://postgres@192.168.99.100/einhorn_starter
* PGAdmin: http://192.168.99.100:5050/
* Local Jenkins: http://192.168.99.100:8090/

## Asynchronous tasks

Asynchronous tasks are used for taks, which really run asynchronous - for example bills, which are created in the background and then send to a user.

We are using RabbitMQ / CloudAMQP as a message broker and Nameko for prodiving the services.

## Websockets & django-channels

This is used for asynchronous, but more directly tasks - like messages to the user or an activity stream. 

## SSL (letsencrypt)

Checkout cookiecutter!

# Old stuff

## Strategic Basics

* I have several ideas and we need a template, we can use as a base instead of doing over and over again
* Things I would build out of it:
 * A product page to advertise + test ideas. A onepage landingpage with an introduction, a form, a newsletter signup, A/B-testing and Adwords + FB ads integration
 * The market place for products and companies with profile pages for each product and the possibility to order or buy things - with statistics and logins for either stakeholder.
 * ...

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


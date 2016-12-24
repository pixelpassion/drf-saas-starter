# Einhornmanufaktur Boilerplate

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

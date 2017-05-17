# Project setup

## Clone the Repository and set it up locally

For existing repositories, simply add the heroku remote

```
$ git clone https://github.com/jensneuhaus/einhorn-starter.git
$ ./local_setup {{project_name}}        # Will create a database and an virtual environment folder .venv
$ source .venv/bin/activate             # Start the virtual environment
$ pip install fabric3                   # Installs fabric3
$ fab update                            # Updates requirements and migrations etc.
```

## Create an heroku app

Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line)

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```
$ heroku login
```

Create a new Heroku app
```
$ git remote set-url origin git://new.url.here                  # Add an new created .git
$ fab create_heroku_app:cool-new-app
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

## SSL with letsencrypt

```
sudo certbot certonly --manual

heroku config:set ACME_TOKEN=
heroku config:set ACME_KEY=

sudo heroku certs:add /etc/letsencrypt/live/starter.einhornmanufaktur.de/fullchain.pem /etc/letsencrypt/live/starter.einhornmanufaktur.de/privkey.pem --app einhorn-starter

heroku config:set SECURE_SSL_REDIRECT=True

```

## Sentry

Errors are pushed to Sentry. Update the SENTRY_DSN setting in the .env

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

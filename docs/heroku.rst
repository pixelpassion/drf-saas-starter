Heroku
============

Requirements
--------------------

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

### Using an existing Heroku app

```
$ heroku git:clone -a cool-new-app
```



Deployment
--------------------

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




Procfile
--------------------



runtime.txt
--------------------

.slugignore
--------------------

app.json
--------------------


Domains & SSL
--------------------

#### Setup domains and an SSL certificate:

Heroku takes care of SSL automatically for paid dynos. Check the [anncouncement](https://blog.heroku.com/announcing-automated-certificate-management) or the [help page](https://devcenter.heroku.com/articles/automated-certificate-management).

Enable certificates for an old app (it is automatically activated for old ones)::

    heroku certs:auto:enable -a cool-new-app

Add a domain::

    heroku domains:add test.yourdomain.de

Afterwards you have to set your DNS provider to the given domain,


You can check the status of domains & SSL::

    heroku domains                                              # Checks all domains
    heroku certs:auto                                           # Checks the status of the automated SSL handling


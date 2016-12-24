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

```
$ git remote set-url origin git://new.url.here                  # Add an new created .git
$ fab create_heroku_app:cool-new-app
```


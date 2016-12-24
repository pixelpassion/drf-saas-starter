# -*- coding: utf-8 -*-
import os
import random

from fabric.api import env, lcd, local, task


def _relative_to_fabfile(*path):
    return os.path.join(os.path.dirname(env.real_fabfile), *path)


@task
def clean():
    """Remove all generated files (.pyc, .coverage, .egg, etc)."""
    with lcd(_relative_to_fabfile()):
        local('find . -name "*.pyc" -exec rm -rf {} \;')
        local('find . -name ".coverage" -exec rm -rf {} \;')
        local('find . -name ".DS_Store" -exec rm -rf {} \;')
        local('find . -name "._DS_Store" -exec rm -rf {} \;')
        local('find . -name "._*.*" -exec rm -rf {} \;')
        local('rm -f .coverage.*')
        local('rm -rf build')
        local('rm -rf dist')


@task
def flake8():
    """Use flake8 to check Python style, PEP8, and McCabe complexity.
    See http://pypi.python.org/pypi/flake8/
    .. note::
        * Files with the following header are skipped::
            # flake8: noqa
        * Lines that end with a ``# NOQA`` comment will not issue a warning.
    """
    local(
        'flake8 '
        '--exclude=".svn,CVS,.bzr,.hg,.git,migrations,__pycache__,._*" '
        '--max-complexity=9 .'
        '--ignore=E501'
    )


@task
def isort():
    """Use isort to automatically (re-)order the import statements on the top of files"""
    with lcd(_relative_to_fabfile()):
        local('isort -rc .')


@task
def build():
    """Prepares the code to be commited"""
    clean()
    isort()
    flake8()
    test()


@task
def test():
    local('python manage.py test')


@task
def commit(message):
    build()
    local('git add .')
    local('git commit -m "%s"' % message)


@task
def push():
    local('git push')


@task
def commit_and_push(message):
    build()
    commit(message)
    push()


@task
def test():
    local('python manage.py test')


@task
def coverage():
    local('coverage run manage.py test')
    local('coverage html')


@task
def update():
    """ Local setup for a new developer """

    if "VIRTUAL_ENV" not in os.environ:
        print("No virtual env found - please run:")
        print("$ ./local_setup.py {{ project_name }}")
        print("$ source .venv/bin/activate")

    local('pip install --upgrade pip setuptools')
    local('pip install -r requirements/local.txt')
    local('python manage.py migrate')


@task
def pull_and_update(branch="master"):
    local("git checkout %s" % branch)
    local("git pull %s" % branch)
    update()


@task
def push_to_heroku():
    local("git push heroku master")
    local('heroku run "python manage.py migrate" --app einhorn-starter')


@task
def docker():
    local("docker-compose -f dev.yml build")
    local("docker-compose -f dev.yml up")


@task
def doc():
    """ Creates the sphinx documnentation for a new developer """

    local('sphinx-apidoc . -o docs/ -f */migrations/*')
    with lcd("docs"):
        local('make html')


@task
def create_heroku_app(app_name):

    local('heroku create %s --buildpack https://github.com/heroku/heroku-buildpack-python  --region eu' % app_name)

    # Attach addons from einhorn-default
    local('heroku addons:attach cloudamqp-opaque-72597 --app %s' % app_name)
    local('heroku addons:attach postgresql-acute-80214 --app %s' % app_name)
    local('heroku addons:attach redis-octagonal-12968 --app %s' % app_name)
    local('heroku addons:attach librato-flat-96442 --app %s' % app_name)

    # Enabling the labs
    local('heroku labs:enable log-runtime-metrics --app %s' % app_name)
    local('heroku labs:enable runtime-dyno-metadata --app %s' % app_name)

    # Setting up backups
    local('heroku pg:backups schedule DATABASE_URL --at "02:00 UTC" --app %s' % app_name)

    # Setting up config
    local('heroku config:set ADMIN_URL="$(openssl rand -base64 32)" '
          'PYTHONHASHSEED=random '
          'SECRET_KEY="$(openssl rand -base64 64)" '
          'ALLOWED_HOSTS=%s.herokuapp.com --app %s' % (app_name, app_name))

    local('heroku git:remote --app %s' % app_name)

    #local('heroku config:set SENTRY_DSN=%s --app %s' % (os.getenv('SENTRY_DSN'), app_name))

    #
    # local('heroku run python manage.py createsuperuser --app %s' % app_name)


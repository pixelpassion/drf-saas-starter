import sys
import os
import subprocess
import json
import random


def create_database(project_name):

    return_code = os.system("createdb " + project_name)
    if return_code != 0:
        return return_code

    print("Created new database {}!".format(project_name))

    return 0


def create_venv():

    return_code = os.system("python3 -m venv .venv")
    if return_code != 0:
        return return_code

    print("Created .venv!")

    return_code = os.system("source .venv/bin/activate")
    if return_code != 0:
        return return_code


    # Activating venv right away in a python script (and using it) does not work, we do it with fabric for now

    # http://devmartin.com/blog/2015/02/how-to-deploy-a-python3-wsgi-application-with-apache2-and-debian/
    # https://www.pythonanywhere.com/forums/topic/994/

    # activate_this_file = ".venv/bin/activate_this.py"
    # with open(activate_this_file) as f:
    #     code = compile(f.read(), activate_this_file, 'exec')
    #     exec(code, dict(__file__=activate_this_file))
    #
    #
    # print("Activated environment")
    #
    # return_code = os.system("pip install --upgrade pip setuptools")
    # if return_code != 0:
    #     return return_code

    return 0


def docker_setup():

    # return_code = os.system("eval $(docker-machine env)")
    # if return_code != 0:
    #     return return_code
    #
    # return_code = os.system("docker-compose -f dev.yml build")
    # if return_code != 0:
    #     return return_code

    return 0


def generate_secret_key():

    return ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])


def main(argv):

    if len(sys.argv) != 2:
        print("ERROR: Incorrect number of args!")
        print("This command takes zero argument exactly:")
        print("name:   the name of the project to be created")
        return 1

    project_name = sys.argv[1]

    # return_code = create_database(project_name)
    # if return_code != 0:
    #     print("Creation of the database failed!")
    #     return 2

    return_code = create_venv()
    if return_code != 0:
        print("Creation of the the virtual env failed!")
        return 3

    return_code = docker_setup()
    if return_code != 0:
        print("Docker setup failed!")
        return 4

    print("")
    print("")
    print("Please use the following entries for your local .env")

    print("")
    print("DEBUG=True")
    print("STAGE=local")
    print("ALLOWED_HOSTS='*'")
    print("DATABASE_URL=postgres:///{}".format(project_name))
    print("SECRET_KEY='{}'".format(generate_secret_key()))


if __name__ == '__main__':
    sys.exit(main(sys.argv))

import sys
import os
import subprocess
import platform
import json
import random
import venv

class EinhornEnvBuilder(venv.EnvBuilder): 
    """
    This builder configures a virtualenv for use with EinhornStarter.

    Currently: It installs requirements.txt file after venv setup. 
    
    This class may be easily modified to add more post-setup configuration steps.
    """

    # Constructor
    def __init__(self, requirements_path, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        self.requirements_path = requirements_path

    # Helper methods for pip and pip install
    def pip(self, context, *args): 
        output = subprocess.check_output([context.env_exe, '-m', 'pip'] + list(args))
        print(str(output.decode()))

    def pip_install(self, context, *args): 
        self.pip(context, 'install', *args)

    # This method is run after the virtualenv is created
    def post_setup(self, context): 
        super().post_setup(context)

        # Make sure pip is up-to-date
        self.pip_install(context, '--upgrade', 'pip')
        self.pip_install(context, '--upgrade', 'setuptools')

        # Install requirements.txt file
        if self.requirements_path: 
            self.pip_install(context, '-r', self.requirements_path)

def create_database(project_name):

    try:
         subprocess.check_output(["createdb", project_name])
    except subprocess.CalledProcessError as e:
        pass
    else:
        print("Database '{}' was created.".format(project_name))



def create_venv(requirements_path):
    """ Creates venv and pip installs everything in the environment """

    if os.path.exists(".venv"):
        print(".venv folder already exists! Skipping.")
        return

    print("Creating virtual environment... - please wait (may take some time)...")
    venv = EinhornEnvBuilder(requirements_path, with_pip=True)
    venv.create(os.path.join(os.getcwd(), '.venv'))

# def setup_docker():
    # return_code = os.system("eval $(docker-machine env)")
    # if return_code != 0:
    #     return return_code
    #
    # return_code = os.system("docker-compose -f dev.yml build")
    # if return_code != 0:
    #     return return_code
#   return 0


def create_env_file(project_name): 
    """ Creates an .env file - if one is not existing already"""
    def generate_secret_key():
        return ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

    env_file_name = ".env"
    env_path = os.path.join(os.getcwd(), env_file_name)

    try: 
        with open(env_path, 'x') as env_file: 
            print("The .env file will be created at: {}".format(env_path))

            env_file.write("DEBUG=True\n")
            env_file.write("STAGE=local\n")
            env_file.write("ALLOWED_HOSTS='*'\n")
            env_file.write("DATABASE_URL=postgres:///{}\n".format(project_name))
            env_file.write("SECRET_KEY='{}'\n".format(generate_secret_key()))

    except FileExistsError:
        print(".env file already exists. Skipping .env creation")


def main(argv):

    if len(sys.argv) != 2:
        print("ERROR: Incorrect number of args!")
        print("This command takes zero argument exactly:")
        print("name:   the name of the project to be created")
        return 1
    project_name = sys.argv[1]

    # Maybe some project name validation checking here

    requirements_path = os.path.join(os.getcwd(), 'requirements/local.txt')

    try: 
        create_database(project_name)
        create_venv(requirements_path)
#       setup_docker()
        create_env_file(project_name)
    except subprocess.CalledProcessError as e:
        print("Command: {}\nReturn code: {}\n{}\n{}".format(e.cmd, 
                                                            e.return_code, 
                                                            e.output, 
                                                            e.stderr))

    # Everything worked!
    print("Done!")
    print("")
    print("")
    print("Please run:")
    print("source .venv/bin/activate")
    print("fab update")
    print("python manage.py createsuperuser")
    print("python manage.py runserver")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

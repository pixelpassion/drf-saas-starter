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

        # Install requirements.txt file
        if self.requirements_path: 
            self.pip_install(context, '-r', self.requirements_path)

        # Show what was installed
        print("Installed packages:")
        self.pip(context, 'freeze')
        

# create database
# def create_database(project_name):
#    output = subprocess.check_output(["createdb", project_name])
#    print(output)
#    print("Created new database {}!".format(project_name))

# Creates venv and pip installs everything in the environment
def create_venv(requirements_path):
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

def generate_secret_key():
    return ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

def create_env_file(project_name): 
    print("")
    print("")
    print("Please use the following entries for your local .env")

    print("")
    print("DEBUG=True")
    print("STAGE=local")
    print("ALLOWED_HOSTS='*'")
    print("DATABASE_URL=postgres:///{}".format(project_name))
    print("SECRET_KEY='{}'".format(generate_secret_key()))



def main(argv):

    if len(sys.argv) != 2:
        print("ERROR: Incorrect number of args!")
        print("This command takes zero argument exactly:")
        print("name:   the name of the project to be created")
        return 1
    project_name = sys.argv[1]

    # Maybe some project name validation checking here

    requirements_path = os.path.join(os.getcwd(), 'requirements.txt')

    print("Working... please wait...")

    try: 
#       create_database(project_name)
        create_venv(requirements_path)
#       setup_docker()
        create_env_file(project_name)
    except subprocess.CalledProcessError as e:
        print("Command: {}\nReturn code: {}\n{}\n{}".format(e.cmd, 
                                                            e.return_code, 
                                                            e.output, 
                                                            e.stderr))

    # It worked!
    print("Done!")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

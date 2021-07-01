# using a .env file (ignored from github) to store environment variable to automatically load using decouple.config
# https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5

# Standard Library imports
import os
import logging

# Third-party imports
from decouple import config


class LocalExecHelper:

    def __init__(self):
        self.load_env_var()

    def load_env_var(self):

        logging.debug("setting local environment variables...")

        # protecting local execution, if databse is not the test's one
        # in exceptional local execution case, this code may have to be commented
        if "test" not in config('MONGODB_NAME'):
            raise Exception
        
        # setting required environment variables
        os.environ["SA_PROJECT_ID"] = config('SA_PROJECT_ID')
        os.environ["SA_PRIVATE_KEY_ID"] = config('SA_PRIVATE_KEY_ID')
        os.environ["SA_PRIVATE_KEY"] = config('SA_PRIVATE_KEY').replace("\\n", "\n")
        os.environ["SA_CLIENT_EMAIL"] = config('SA_CLIENT_EMAIL')
        os.environ["SA_CLIENT_ID"] = config('SA_CLIENT_ID')
        os.environ["SA_CLIENT_X509_CERT_URL"] = config('SA_CLIENT_X509_CERT_URL')

        os.environ["MONGODB_USER"] = config('MONGODB_USER')
        os.environ["MONGODB_PWD"] = config('MONGODB_PWD')
        os.environ["MONGODB_NAME"] = config('MONGODB_NAME')


# automatically loading local environment variables if local context detected
try:

    os.environ["MONGODB_NAME"]
    logging.info("Using provided environment variables.")

except KeyError:

    LocalExecHelper()
    logging.info("Using local variables from .env file.")

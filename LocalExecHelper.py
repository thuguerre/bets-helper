# using a .env file (ignored from github) to store environment variable to automatically load using decouple.config
# https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5

import logging
import os
from decouple import config


class LocalExecHelper:

    def __init__(self):
        self.load_env_var()

    def load_env_var(self):

        logging.debug("setting local environment variables")

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

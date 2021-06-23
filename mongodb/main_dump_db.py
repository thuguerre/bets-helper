from BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper
import logging
import sys
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    delete_files = False

    # loading script arguments
    for args in sys.argv:

        if args == "local_exec":
            LocalExecHelper()
        
        elif args == "delete_files:yes":
            delete_files = True

    # dumping MongoDB to files
    logging.info("dumping mongodb...")
    mongodb = BetsMongoDB()
    files = mongodb.dumpDB()
    logging.info("dumped.")

    # use creds to create a client to interact with the Google Drive API
    credentials = {
        "type": "service_account",
        "project_id": os.environ["SA_PROJECT_ID"],
        "private_key_id": os.environ["SA_PRIVATE_KEY_ID"],
        "private_key": os.environ["SA_PRIVATE_KEY"],
        "client_email": os.environ["SA_CLIENT_EMAIL"],
        "client_id": os.environ["SA_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ["SA_CLIENT_X509_CERT_URL"]
    }

    # connecting to Google Drive
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    drive = GoogleDrive(gauth)

    for upload_file in files:
	    gfile = drive.CreateFile()
	    gfile.SetContentFile(upload_file)
	    gfile.Upload()

    # deleting files if asked
    if delete_files:
        for delete_file in files:
            os.remove(delete_file)

        logging.info("files deleted")

    logging.info("mongodb dumped and uploaded")

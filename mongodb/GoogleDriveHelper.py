import os
import typing
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

class GoogleDriveHelper:

    drive = None

    def __init__(self):

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
        self.drive = GoogleDrive(gauth)

    def upload_files(self, files: typing.List[str], backup_folder_name: str = ""):

        for upload_file in files:
            gfile = self.drive.CreateFile({'title': upload_file})
            gfile.SetContentFile(backup_folder_name + upload_file)
            gfile.Upload()

    def download_files(self, prefix: str = "", backup_folder_name: str = "") -> typing.List[str]:

        if not(backup_folder_name == ""):
            # creating BACKUP folder if it does not exists
            Path(backup_folder_name).mkdir(exist_ok=True)

        downloaded_files = []

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

        for drive_file in file_list:

            if drive_file['title'].startswith(prefix):
                file = self.drive.CreateFile({'id': drive_file['id']})
                file.GetContentFile(backup_folder_name + drive_file['title'])
                downloaded_files.append(drive_file['title'])

        return downloaded_files

    def delete_files(self, prefix: str = ""):

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for drive_file in file_list:
            if drive_file['title'].startswith(prefix):
                file = self.drive.CreateFile({'id': drive_file['id']})
                file.Trash()

    def delete_all_files(self):
        self.delete_files("")

    def list_files(self):

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for drive_file in file_list:
            print(drive_file['title'])

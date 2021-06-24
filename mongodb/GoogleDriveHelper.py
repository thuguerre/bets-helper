import os
import typing
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


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

    def upload_files(self, files: typing.List[str]):

        for upload_file in files:
            file_id = self.get_file_id_by_name(upload_file)

            if file_id == "":
                gfile = self.drive.CreateFile()
            else:
                gfile = self.drive.CreateFile({'id': file_id})

            gfile.SetContentFile(upload_file)
            gfile.Upload()

    def get_file_id_by_name(self, name: str) -> str:

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for drive_file in file_list:
            if drive_file['title'] == name:
                return drive_file['id']

        return ""

    def download_files(self, prefix: str = "") -> typing.List[str]:

        downloaded_files = []

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for drive_file in file_list:
            if drive_file['title'].startswith(prefix):
                file = self.drive.CreateFile({'id': drive_file['id']})
                file.GetContentFile(drive_file['title'])
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

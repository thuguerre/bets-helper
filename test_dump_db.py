import pytest
import unittest
import os
from pathlib import Path
from mongodb.GoogleDriveHelper import GoogleDriveHelper
from LocalExecHelper import LocalExecHelper
from datetime import datetime
import glob
import re


BACKUP_FOLDER_NAME = "./backup/"

class TestDumpDB(unittest.TestCase):

    drive = None

    def setUp(self):
        
        try:
            os.environ["MONGODB_NAME"]
        except KeyError:
            LocalExecHelper()

        self.__prepare_backup_folder()
        self.__test_is_backup_folder_empty()

        self.drive = GoogleDriveHelper()

        self.__prepare_drive_folder()
        self.__test_is_gdrive_folder_empty()

    def tearDown(self):
        self.__prepare_backup_folder() # deleting files
        self.__delete_backup_folder() # deleting empty folder

    def __test_is_backup_folder_empty(self):
        self.assertTrue(os.listdir(BACKUP_FOLDER_NAME) == [])

    def __test_number_files_in_backup_folder(self, number_of_files: int):
        self.assertEqual(len(os.listdir(BACKUP_FOLDER_NAME)), number_of_files)

    def __test_is_gdrive_folder_empty(self):
        self.assertEqual(self.drive.count_files(os.environ["MONGODB_NAME"]), 0)
    
    def __test_number_files_in_gdrive_folder(self, number_of_files: int):
        self.assertEqual(self.drive.count_files(os.environ["MONGODB_NAME"]), 1)

    def __prepare_backup_folder(self):

        # creating BACKUP folder if it does not exists
        Path(BACKUP_FOLDER_NAME).mkdir(exist_ok=True)

        # deleting all files from pre-existing backup folder
        for file_to_delete in os.listdir(BACKUP_FOLDER_NAME):
            os.remove(os.path.join(BACKUP_FOLDER_NAME, file_to_delete))

    def __delete_backup_folder(self):
        os.rmdir(BACKUP_FOLDER_NAME)

    def __prepare_drive_folder(self):
        self.drive.delete_files(os.environ["MONGODB_NAME"])

    def __test_exist_backup_file_in_backup_folder(self, collection_name: str):
        now = datetime.now()
        self.assertEqual(
            len(
                glob.glob(
                    BACKUP_FOLDER_NAME
                    + os.environ["MONGODB_NAME"]
                    + '.'
                    + collection_name
                    + '.'
                    + now.strftime("%Y%m%d%H%M")
                    + '*.json')
                ),
            1
        )

    def __test_exist_backup_file_in_gdrive_folder(self, collection_name: str):
        file_found = False
        now = datetime.now()
        regex = re.compile(os.environ["MONGODB_NAME"] + '.' + collection_name + '.' + now.strftime("%Y%m%d%H%M") + '[0-9]{2}.json')
        drive_files = self.drive.list_files(os.environ["MONGODB_NAME"])
        for drive_file in drive_files:
            if regex.match(drive_file):
                file_found = True
        self.assertTrue(file_found)    

    @pytest.mark.unittest
    def test_backup_file_is_generated(self):
        
        # dumping a file, without uploading it and deleting it
        os.system("python3 ./mongodb/main_dump_db.py upload_to_gdrive:no delete_local_files:no")

        self.__test_number_files_in_backup_folder(1)
        self.__test_exist_backup_file_in_backup_folder('match_results')

        self.__test_is_gdrive_folder_empty()

    @pytest.mark.unittest
    def test_backup_file_is_generated_and_locally_deleted(self):
        
        # dumping a file, without uploading it and deleting it
        os.system("python3 ./mongodb/main_dump_db.py upload_to_gdrive:no delete_local_files:yes")

        self.__test_is_backup_folder_empty()
        self.__test_is_gdrive_folder_empty()

    @pytest.mark.unittest
    def test_backup_file_is_uploaded(self):
        
        # dumping a file, without uploading it and deleting it
        os.system("python3 ./mongodb/main_dump_db.py upload_to_gdrive:yes delete_local_files:no")

        self.__test_number_files_in_backup_folder(1)
        self.__test_exist_backup_file_in_backup_folder('match_results')

        self.__test_number_files_in_gdrive_folder(1)
        self.__test_exist_backup_file_in_gdrive_folder('match_results')

    @pytest.mark.unittest
    def test_backup_file_is_uploaded_and_locally_delete(self):
        
        # dumping a file, without uploading it and deleting it
        os.system("python3 ./mongodb/main_dump_db.py upload_to_gdrive:yes delete_local_files:yes")

        self.__test_is_backup_folder_empty()

        self.__test_number_files_in_gdrive_folder(1)
        self.__test_exist_backup_file_in_gdrive_folder('match_results')

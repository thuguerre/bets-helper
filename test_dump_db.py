import pytest
import unittest
import os
from pathlib import Path
from mongodb.GoogleDriveHelper import GoogleDriveHelper
from LocalExecHelper import LocalExecHelper

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

    @pytest.mark.unittest
    def test_backup_file_generated(self):
        
        # dumping a file, without uploading it and deleting it
        os.system("python3 ./mongodb/main_dump_db.py upload_to_gdrive:no delete_local_files:no")

        self.__test_number_files_in_backup_folder(1)
        # TODO testing local name file
        self.__test_is_gdrive_folder_empty()

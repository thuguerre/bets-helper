# Standard Library imports
import os
import pytest
import unittest
from pathlib import Path
from datetime import datetime
import glob

# Local imports
import localcontextloader
from mongodb.GoogleDriveHelper import GoogleDriveHelper
from mongodb.BetsMongoDB import BetsMongoDB
import main_dump_db


class TestDumpDB(unittest.TestCase):

    drive = None
    mongodb_name = None
    backup_folder_name = None

    def setUp(self):

        self.mongodb_name = os.environ["MONGODB_NAME"]
        self.backup_folder_name = main_dump_db.BACKUP_FOLDER_NAME

        self.prepare_backup_folder()
        self.assert_root_backup_folder_is_empty()

        self.drive = GoogleDriveHelper()

        self.prepare_drive_folder()
        self.assert_gdrive_folder_is_empty()

    def tearDown(self):
        self.prepare_backup_folder() # deleting files
        self.delete_backup_folder() # deleting empty folder

    def get_db_backup_folder_path(self):
        return f"{self.backup_folder_name}{self.mongodb_name}/"

    def assert_root_backup_folder_is_empty(self):
        self.assertTrue(os.listdir(self.backup_folder_name) == [])
    
    def assert_gdrive_folder_is_empty(self):
        self.assertEqual(len(self.drive.list_files(self.mongodb_name)), 0)
    
    def prepare_backup_folder(self):

        # creating BACKUP folder if it does not exists
        Path(self.backup_folder_name).mkdir(exist_ok=True)

        db_backup_folder_path = self.get_db_backup_folder_path()

        if os.path.isdir(db_backup_folder_path):

            # deleting all files from pre-existing backup folder
            for file_to_delete in os.listdir(db_backup_folder_path):
                os.remove(os.path.join(db_backup_folder_path, file_to_delete))

            os.rmdir(db_backup_folder_path)

        # deleting all files from pre-existing backup folder
        for file_to_delete in os.listdir(self.backup_folder_name):
            os.remove(os.path.join(self.backup_folder_name, file_to_delete))

    def delete_backup_folder(self):
        os.rmdir(self.backup_folder_name)

    def prepare_drive_folder(self):
        self.drive.delete_files(self.mongodb_name)

    def get_collection_metadata_dump_filename(self, collection_name: str):
        return f"{self.mongodb_name}#*#{collection_name}.metadata.json"

    def get_collection_bson_dump_filename(self, collection_name: str):
        return f"{self.mongodb_name}#*#{collection_name}.bson"

    def get_collection_metadata_dump_path(self, collection_name: str):
        return self.backup_folder_name + self.get_collection_metadata_dump_filename(collection_name)

    def get_collection_bson_dump_path(self, collection_name: str):
        return self.backup_folder_name + self.get_collection_bson_dump_filename(collection_name)

    def assert_all_backup_files_are_in_local_folder(self):
        
        # verify DB backup folder exists
        self.assertTrue(os.path.isdir(self.backup_folder_name))

        # verify all backup files exist for collection 'matches'
        self.assertEqual(len(glob.glob(self.get_collection_metadata_dump_path('matches'))), 1)
        self.assertEqual(len(glob.glob(self.get_collection_bson_dump_path('matches'))), 1)

    def assert_all_backup_files_are_in_gdrive_folder(self):

        # get all files from gdrive, with mongodb name prefix
        gdrive_files = self.drive.list_files(self.mongodb_name)

        # expecting 2 files, both for matches collection
        self.assertEquals(len(gdrive_files), 2)

        matches_json_found = False
        matches_bson_found = False

        for filename in gdrive_files:

            if filename.startswith(self.mongodb_name + "#") and filename.endswith("#matches.metadata.json"):
                matches_json_found = True

            if filename.startswith(self.mongodb_name + "#") and filename.endswith("#matches.bson"):
                matches_bson_found = True

        self.assertTrue(matches_json_found)
        self.assertTrue(matches_bson_found)

    def assert_db_backup_folder_does_not_exist(self):
        self.assertFalse(os.path.exists(self.backup_folder_name + self.mongodb_name))

    def assert_root_backup_folder_does_not_exist(self):
        self.assertFalse(os.path.exists(self.backup_folder_name))

    def test_backup_files_are_generated(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:no delete_local_files:no")

        self.assert_db_backup_folder_does_not_exist()
        self.assert_all_backup_files_are_in_local_folder()
        self.assert_gdrive_folder_is_empty()

    def test_backup_files_are_generated_and_locally_deleted(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:no delete_local_files:yes")

        self.assert_db_backup_folder_does_not_exist()
        self.assert_root_backup_folder_does_not_exist()
        self.assert_gdrive_folder_is_empty()
 
    def test_backup_file_is_uploaded(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:yes delete_local_files:no")

        self.assert_db_backup_folder_does_not_exist()
        self.assert_all_backup_files_are_in_local_folder()
        self.assert_all_backup_files_are_in_gdrive_folder()

    def test_backup_files_are_uploaded_and_locally_deleted(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:yes delete_local_files:yes")

        self.assert_db_backup_folder_does_not_exist()
        self.assert_root_backup_folder_does_not_exist()
        self.assert_all_backup_files_are_in_gdrive_folder()

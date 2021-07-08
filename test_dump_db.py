# Standard Library imports
import os
import pytest
import unittest
from pathlib import Path
from datetime import datetime
import glob
import re
import random

# Local imports
import localcontextloader
from mongodb.GoogleDriveHelper import GoogleDriveHelper
from mongodb.BetsMongoDB import BetsMongoDB
from betsmodels import Match
from betsmodels import Sport
from betsmodels import Country
from betsmodels import Bookmaker
import main_dump_db


class TestDumpDB(unittest.TestCase):

    drive = None
    mongodb_name = None
    BACKUP_FOLDER_NAME = None

    def setUp(self):

        self.mongodb_name = os.environ["MONGODB_NAME"]
        self.BACKUP_FOLDER_NAME = main_dump_db.BACKUP_FOLDER_NAME

        self.__prepare_backup_folder()
        self.__test_is_root_backup_folder_empty()

        self.drive = GoogleDriveHelper()

        self.__prepare_drive_folder()
        self.__test_is_gdrive_folder_empty()

    def tearDown(self):
        self.__prepare_backup_folder() # deleting files
        self.__delete_backup_folder() # deleting empty folder

    def __get_db_backup_folder_path(self):
        return f"{self.BACKUP_FOLDER_NAME}{self.mongodb_name}/"

    def __test_root_backup_folder_is_empty(self):
        self.assertTrue(os.listdir(self.BACKUP_FOLDER_NAME) == [])
    
    def __test_is_db_backup_folder_empty(self):
        self.assertTrue(os.listdir(self.__get_db_backup_folder_path()) == [])

    def __test_number_files_in_db_backup_folder(self, number_of_files: int):
        self.assertEqual(len(os.listdir(self.__get_db_backup_folder_path())), number_of_files)

    def __test_gdrive_folder_is_empty(self):
        #TODO le backup folder doit être préfixé par le nom de la BDD
        self.assertEqual(self.drive.count_files(self.mongodb_name), 0)
    
    def __test_number_files_in_gdrive_folder(self, number_of_files: int):
        self.assertEqual(self.drive.count_files(self.mongodb_name), number_of_files)

    def __prepare_backup_folder(self):

        # creating BACKUP folder if it does not exists
        Path(self.BACKUP_FOLDER_NAME).mkdir(exist_ok=True)

        if os.path.isdir(self.BACKUP_FOLDER_NAME + "bets_test_db/") :
            # deleting all files from pre-existing backup folder
            for file_to_delete in os.listdir(self.BACKUP_FOLDER_NAME + "bets_test_db/"):
                os.remove(os.path.join(self.BACKUP_FOLDER_NAME + "bets_test_db/", file_to_delete))

            os.rmdir(self.BACKUP_FOLDER_NAME + "bets_test_db/")

        # deleting all files from pre-existing backup folder
        for file_to_delete in os.listdir(self.BACKUP_FOLDER_NAME):
            os.remove(os.path.join(self.BACKUP_FOLDER_NAME, file_to_delete))

    def __delete_backup_folder(self):
        os.rmdir(self.BACKUP_FOLDER_NAME)

    def __prepare_drive_folder(self):
        self.drive.delete_files(self.mongodb_name)

    def __test_exist_backup_file_in_gdrive_folder(self, collection_name: str):
        file_found = False
        regex = re.compile(self.__get_dump_filename_pattern(collection_name))
        drive_files = self.drive.list_files(self.mongodb_name)
        for drive_file in drive_files:
            if regex.match(drive_file):
                file_found = True
        self.assertTrue(file_found)

    def __get_collection_metadata_dump_filename(self, collection_name: str):
        return f"{self.mongodb_name}/{collection_name}.metadata.json"

    def __get_collection_bson_dump_filename(self, collection_name: str):
        return f"{self.mongodb_name}/{collection_name}.bson"

    def __get_collection_metadata_dump_path(self, collection_name: str):
        return self.BACKUP_FOLDER_NAME + self.__get_collection_metadata_dump_filename(collection_name)

    def __get_collection_bson_dump_path(self, collection_name: str):
        return self.BACKUP_FOLDER_NAME + self.__get_collection_bson_dump_filename(collection_name)

    def __test_all_backup_files_are_in_local_folder(self):
        
        # verify DB backup folder exists
        self.assertTrue(os.path.isdir(self.BACKUP_FOLDER_NAME + "bets_test_db/"))

        # verify all backup files exist for collection 'matches'
        self.assertEqual(len(glob.glob(self.__get_collection_metadata_dump_path('matches'))), 1)
        self.assertEqual(len(glob.glob(self.__get_collection_bson_dump_path('matches'))), 1)

    @pytest.mark.unittest
    def test_backup_file_is_generated(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:no delete_local_files:no")

        self.__test_all_backup_files_are_in_local_folder()
        self.__test_is_gdrive_folder_empty()

    @pytest.mark.unittest
    def test_backup_file_is_generated_and_locally_deleted(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:no delete_local_files:yes")

        self.__test_root_backup_folder_is_empty()
        self.__test_gdrive_folder_is_empty()
 
    @pytest.mark.unittest
    def test_backup_file_is_uploaded(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:yes delete_local_files:no")

        self.__test_all_backup_files_are_in_local_folder()

        self.__test_number_files_in_gdrive_folder(2)
        self.__test_exist_backup_file_in_gdrive_folder('matches')

"""
    @pytest.mark.unittest
    def test_backup_file_is_uploaded_and_locally_deleted(self):
        
        os.system("python3 ./main_dump_db.py upload_to_gdrive:yes delete_local_files:yes")

        self.__test_is_backup_folder_empty()

        self.__test_number_files_in_gdrive_folder(1)
        self.__test_exist_backup_file_in_gdrive_folder('matches')

    @pytest.mark.unittest
    def test_content_backup_file(self):

        # preparing random match to insert in db, so in dump
        match = Match(
            datetime.now(),
            Sport.BASEBALL,
            Country.JAPAN,
            "Regular Season",
            datetime.now(),
            Bookmaker.WINAMAX,
            str(random.randint(0,99)),
            'test_content_backup_file_home_team' + str(random.randint(0,99)),
            str(random.randint(0,99)),
            None,
            'test_content_backup_file_visitor_team' + str(random.randint(0,99)),
            str(random.randint(0,99)),
            None
        )

        mongodb = BetsMongoDB()
        mongodb.insertMatchOrAppendOdds(match)

        # dumping the mongo db
        os.system("python3 ./main_dump_db.py upload_to_gdrive:no delete_local_files:no")

        # testing the dump files are here
        self.__test_number_files_in_backup_folder(1)
        self.__test_exist_backup_file_in_backup_folder('matches')

         # testing the presence of the match in the dump
        matches_backup_filename = glob.glob(self.BACKUP_FOLDER_NAME + self.__get_dump_filename_bson('matches'))[0]
        with open(matches_backup_filename) as matches_backup_file:
            self.assertTrue(match.toMongoDBDataFragment() in matches_backup_file.read())

        # testing no file has been uploaded to Google Drive
        self.__test_is_gdrive_folder_empty()
 """
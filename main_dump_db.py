# Standard Library imports
import os
import sys
import logging
from datetime import date

# Local imports
import localcontextloader
from mongodb.BetsMongoDB import BetsMongoDB
from mongodb.GoogleDriveHelper import GoogleDriveHelper


BACKUP_FOLDER_NAME = "./backup-" + date.today().strftime("%Y-%m-%d") + "/"

#
# Documentation Printing Method
#
def printDocumentation():

    print("")
    print("args 'upload_to_gdrive:yes|no' to upload files to GDrive. Yes by default.")
    print("args 'delete_local_files:yes|no' to delete locally-dumped files after their upload to GDrive.")
    print("")
    print("Typical use:")
    print("  python3 main_dump_db.py upload_to_gdrive:yes delete_local_files:yes")
    print("")

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    upload_to_gdrive = True
    delete_local_files = False
    delete_remote_files = False
    mongodb_name = os.environ["MONGODB_NAME"]

    # loading script arguments
    for args in sys.argv:

        if args == "delete_local_files:yes":
            delete_local_files = True

        elif args == "delete_local_files:no":
            delete_local_files = False
        
        elif args == "upload_to_gdrive:yes":
            upload_to_gdrive = True

        elif args == "upload_to_gdrive:no":
            upload_to_gdrive = False
        
        elif args == '-h' or args == "-help" or args == "--h" or args == "--help":
            printDocumentation()
            sys.exit()

    # dumping MongoDB to files
    logging.info("dumping mongodb...")
    mongodb = BetsMongoDB()
    files = mongodb.dump_database(BACKUP_FOLDER_NAME)
    logging.info("dumped.")

    # uploading dumped files to Google Drive
    if upload_to_gdrive:

        drive = GoogleDriveHelper()

        # creating the folder what will receive the files
        gdrive_backup_folder_name = mongodb_name + "-backup-" + date.today().strftime("%Y-%m-%d")
        gdrive_folder_id = drive.create_folder(gdrive_backup_folder_name)

        drive.upload_files(files, BACKUP_FOLDER_NAME, gdrive_folder_id)
        logging.info("files uploaded to GDrive")
    
    # deleting files if asked
    if delete_local_files:
        for delete_file in files:
            os.remove(delete_file)

        os.rmdir(BACKUP_FOLDER_NAME + os.environ["MONGODB_NAME"])

        logging.info("files deleted")

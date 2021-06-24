from BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper
import logging
import sys
import os
from GoogleDriveHelper import GoogleDriveHelper


BACKUP_FOLDER_NAME = "./backup/"

#
# Documentation Printing Method
#
def printDocumentation():

    print("")
    print("args 'local_exec' to load required environment variables. Must be first argument, to let others working.")
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

    # loading script arguments
    for args in sys.argv:

        if args == "local_exec":
            LocalExecHelper()
        
        elif args == "delete_local_files:yes":
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
    files = mongodb.dumpDB(BACKUP_FOLDER_NAME)
    logging.info("dumped.")

    # uploading dumped files to Google Drive
    if upload_to_gdrive:
        drive = GoogleDriveHelper()

        drive.upload_files(files, BACKUP_FOLDER_NAME)
        logging.info("files uploaded to GDrive")
    
    # deleting files if asked
    if delete_local_files:
        for delete_file in files:
            os.remove(BACKUP_FOLDER_NAME + delete_file)

        logging.info("files deleted")

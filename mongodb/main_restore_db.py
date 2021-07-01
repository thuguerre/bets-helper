# Standard Library imports
import os
import sys
import logging

# Local imports
import localcontextloader
from BetsMongoDB import BetsMongoDB
from GoogleDriveHelper import GoogleDriveHelper


BACKUP_FOLDER_NAME = "./backup/"

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    delete_local_files = False

    # loading script arguments
    for args in sys.argv:
        if args == "delete_local_files:yes":
            delete_local_files = True

    # downloading files from GDrive
    drive = GoogleDriveHelper()
    download_files = drive.download_files(os.environ["MONGODB_NAME"], BACKUP_FOLDER_NAME)
    
    # deleting files if asked
    if delete_local_files:
        for delete_file in download_files:
            os.remove(delete_file)

        logging.info("files deleted")

from BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper
import logging
import sys
import os
from GoogleDriveHelper import GoogleDriveHelper


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

    # uploading dumped files to Google Drive
    drive = GoogleDriveHelper()
    drive.upload_files(files)
    logging.info("files uploaded to GDrive")
    
    # deleting files if asked
    if delete_files:
        for delete_file in files:
            os.remove(delete_file)

        logging.info("files deleted")

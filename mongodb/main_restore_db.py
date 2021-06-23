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

    # downloading files from GDrive
    drive = GoogleDriveHelper()
    download_files = drive.download_files(os.environ["MONGODB_NAME"])
    
    # deleting files if asked
    if delete_files:
        for delete_file in download_files:
            os.remove(delete_file)

        logging.info("files deleted")

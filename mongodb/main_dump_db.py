from BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper
import logging
import sys
import os
from GoogleDriveHelper import GoogleDriveHelper


#
# Documentation Printing Method
#
def printDocumentation():

    print("")
    print("args 'local_exec' to load required environment variables. Must be first argument, to let others working.")
    print("args 'upload_to_gdrive:yes' to upload files to GDrive. No by default!")
    print("args 'delete_local_files:yes' to delete locally-dumped files after their upload to GDrive.")
    print("args 'delete_remote_files:yes' to delete GDrive BEFORE new upload. Please use carefully.")
    print("")
    print("Typical use:")
    print("  python3 main_dump_db.py upload_to_gdrive:yes delete_local_files:yes delete_remote_files:yes")
    print("")

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    upload_to_gdrive = False
    delete_local_files = False
    delete_remote_files = False

    # loading script arguments
    for args in sys.argv:

        if args == "local_exec":
            LocalExecHelper()
        
        elif args == "delete_local_files:yes":
            delete_local_files = True
        
        elif args == "upload_to_gdrive:yes":
            upload_to_gdrive = True

        elif args == "delete_remote_files:yes":
            delete_remote_files = True
        
        elif args == '-h' or args == "-help" or args == "--h" or args == "--help":
            printDocumentation()
            sys.exit()

    # dumping MongoDB to files
    logging.info("dumping mongodb...")
    mongodb = BetsMongoDB()
    files = mongodb.dumpDB()
    logging.info("dumped.")

    # uploading dumped files to Google Drive
    if upload_to_gdrive:
        drive = GoogleDriveHelper()

        if delete_remote_files:
            logging.debug("deleting files from GDrive")
            drive.delete_files(os.environ["MONGODB_NAME"])

        drive.upload_files(files)
        logging.info("files uploaded to GDrive")
    
    # deleting files if asked
    if delete_local_files:
        for delete_file in files:
            os.remove(delete_file)

        logging.info("files deleted")

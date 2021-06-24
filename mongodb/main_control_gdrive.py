from BetsMongoDB import BetsMongoDB
import logging
import sys
from GoogleDriveHelper import GoogleDriveHelper
from LocalExecHelper import LocalExecHelper


#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.WARN)

    LocalExecHelper()

    list_files = False
    delete_all_files = False

    # loading script arguments
    for args in sys.argv:
        
        if args == "action:list_files":
            list_files = True
        
        elif args == "action:delete_all_files":
            delete_all_files = True

    drive = GoogleDriveHelper()

    if list_files:
        drive.list_files()
        print("----")

    if delete_all_files:
        drive.delete_all_files()
        print("files deleted")
        print("----")

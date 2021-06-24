from BetsMongoDB import BetsMongoDB
import logging
import sys
from GoogleDriveHelper import GoogleDriveHelper
from LocalExecHelper import LocalExecHelper


#
# Documentation Printing Method
#
def printDocumentation():

    print("")
    print("args 'action:list_files' to print all non trashed files on remote GDrive.")
    print("args 'action:delete_test_files' to move to trash all files on remote GDrive.")
    print("args 'action:delete_all_files' to move to trash all files on remote GDrive.")
    print("")

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.WARN)

    LocalExecHelper()

    list_files = False
    delete_all_files = False
    delete_test_files = False

    # loading script arguments
    for args in sys.argv:
        
        if args == "action:list_files":
            list_files = True
        
        elif args == "action:delete_all_files":
            delete_all_files = True

        elif args == "action:delete_test_files":
            delete_test_files = True

        elif args == '-h' or args == "-help" or args == "--h" or args == "--help":
            printDocumentation()
            sys.exit()

    drive = GoogleDriveHelper()

    if list_files:
        drive.list_files()
        print("----")

    if delete_all_files:
        drive.delete_all_files()
        print("files deleted")
        print("----")

    if delete_test_files:
        drive.delete_files("bets_test_db")
        print("test files deleted")
        print("----")

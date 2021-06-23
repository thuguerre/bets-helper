from BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper
import logging
import sys
import os


#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    delete_files = False

    # loading script argument
    for args in sys.argv:

        if args == "local_exec":
            LocalExecHelper()
        
        elif args == "delete_files:yes":
            delete_files = True

    # dumping MongoDB to files
    mongodb = BetsMongoDB()
    files = mongodb.dumpDB()

    # deleting files if asked
    if delete_files:
        for file in files:
            os.remove(file)

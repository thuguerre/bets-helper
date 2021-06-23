from BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper
import logging
import sys

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    # loading script argument
    for args in sys.argv:

        if args == "local_exec":
            LocalExecHelper()

    mongodb = BetsMongoDB()
    mongodb.dumpDB()

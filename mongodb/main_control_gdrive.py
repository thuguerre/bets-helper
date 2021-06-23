from BetsMongoDB import BetsMongoDB
import logging
from GoogleDriveHelper import GoogleDriveHelper
from LocalExecHelper import LocalExecHelper


#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    LocalExecHelper()

    drive = GoogleDriveHelper()
    drive.list_files()

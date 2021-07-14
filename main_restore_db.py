# Standard Library imports
import os
import sys
import logging
from pathlib import Path

# Local imports
import localcontextloader
from mongodb.GoogleDriveHelper import GoogleDriveHelper


BACKUP_FOLDER_NAME = "./dump/"

#
# Documentation Printing Method
#
def printDocumentation():

    print("")
    print("args XXX")
    print("args XXX")
    print("")
    print("Typical use:")
    print("  python3 TODO")
    print("")

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    mongodb_name = os.environ["MONGODB_NAME"]
    drive = GoogleDriveHelper()

    # select database to restore
    backuped_dbs = drive.get_backuped_dbs()

    if len(backuped_dbs) == 0:
        raise "No backuped database found."

    print("")
    print("Backuped databases:")
    for backuped_db in backuped_dbs:
        print("- " + backuped_db)

    print("")
    db_name_to_restore = input("Enter DB name to restore: ")

    if db_name_to_restore not in backuped_dbs:
        raise "DB Name is incorrect"

    # select this database's timestamp to restore
    timestamps = drive.get_backups_timestamps(db_name_to_restore)

    if len(timestamps) == 0:
        raise "No backup found for this database."

    print("")
    print("Timestamps available:")
    for timestamp in timestamps:
        print("- " + timestamp)

    print("")
    timestamp_to_restore = input("Enter timestamp to restore: ")

    if timestamp_to_restore not in timestamps:
        raise "Timestamp is incorrect"

    # download files to restore
    downloaded_file_prefix = f"{db_name_to_restore}#{timestamp_to_restore}#"
    downloaded_files = drive.download_files(downloaded_file_prefix, BACKUP_FOLDER_NAME)
    Path(BACKUP_FOLDER_NAME + db_name_to_restore).mkdir(exist_ok=True)

    for downloaded_file in downloaded_files:
        new_filename = downloaded_file.replace(downloaded_file_prefix, "")
        os.rename(f"{BACKUP_FOLDER_NAME}{downloaded_file}", f"{BACKUP_FOLDER_NAME}{db_name_to_restore}/{new_filename}")

    print("")
    print(f"Downloaded files in '{BACKUP_FOLDER_NAME}{db_name_to_restore}':")
    for downloaded_file in downloaded_files:
        print("- " + downloaded_file + " -> " + downloaded_file.replace(downloaded_file_prefix, ""))

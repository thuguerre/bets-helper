from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime
import sys
from pathlib import Path
import os
import logging

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import MatchResult
from betsmodels import Match

class BetsMongoDB:

    db = None

    def __init__(self):
        mongodb_user = os.environ['MONGODB_USER']
        mongodb_pwd = os.environ['MONGODB_PWD']
        mongodb_name = os.environ['MONGODB_NAME']

        client = MongoClient("mongodb+srv://"+mongodb_user+":"+mongodb_pwd+"@cluster0.gu9bi.mongodb.net/"+mongodb_name+"?retryWrites=true&w=majority")
        self.db = client.get_default_database()

    def insertMatchResult(self, match_result: MatchResult):
        return self.db.match_results.insert_one(match_result.toJSON())

    def insertMatchOrAppendOdds(self, match: Match):

        query = {
            "bookmaker": match.bookmaker,
            "bookmaker_match_id": match.bookmaker_match_id
        }

        existing_matches = self.db.matches.find(query)
        existing_matches = list(existing_matches)

        if len(existing_matches) == 0:
            # no existing match: inserting new one
            return self.db.matches.insert_one(match.toJSON())

        elif len(existing_matches) == 1:
            # existing match: appending odds to existing one
            for odd in match.odds:          
                self.db.matches.find_and_modify(
                    query,
                    update = {
                        "$push": { "odds" : odd.toJSON() }
                    }
                )

        else:
            raise Exception


    def getLastMatchResultDate(self):
        return self.db.match_results.find().sort("date", -1).limit(1).next().get('date')
    
    def dumpDB(self, backup_folder_name: str = ""):
        files = []
        files.append(self.__dumpCollection(self.db.match_results, backup_folder_name))
        files.append(self.__dumpCollection(self.db.matches, backup_folder_name))
        return files

    def __dumpCollection(self, collection, backup_folder_name: str = "") -> str:

        if not(backup_folder_name == ""):
            # creating BACKUP folder if it does not exists
            Path(backup_folder_name).mkdir(exist_ok=True)

        logging.debug("dumping collection '" + collection.full_name + "'")
        dump_filename = self.__define_dump_filename(collection)

        cursor = collection.find({})
        with open(backup_folder_name + dump_filename, 'w') as file:
            file.write('[')
            for document in cursor:
                file.write(dumps(document))
                file.write(',\n')
            file.write(']')

        return dump_filename

    def __define_dump_filename(self, collection) -> str:

        now = datetime.now()
        suffix = now.strftime("%Y%m%d%H%M%S")

        return collection.full_name + '.' + suffix + '.json'

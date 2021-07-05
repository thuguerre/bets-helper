# Standard Library imports
import os
import sys
import logging
from bson.json_util import dumps
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

# Third party imports
from pymongo import MongoClient

# Local imports
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import Match


class BetsMongoDB:

    __db = None

    def __init__(self):
        mongodb_user = os.environ['MONGODB_USER']
        mongodb_pwd = os.environ['MONGODB_PWD']
        mongodb_name = os.environ['MONGODB_NAME']

        client = MongoClient(f"mongodb+srv://{mongodb_user}:{mongodb_pwd}@cluster0.gu9bi.mongodb.net/{mongodb_name}?retryWrites=true&w=majority")
        self.__db = client.get_default_database()

    def insertMatchOrAppendOdds(self, match: Match):

        query = {
            "bookmaker": match.bookmaker,
            "bookmaker_match_id": match.bookmaker_match_id
        }

        existing_matches = self.__db.matches.find(query)
        existing_matches = list(existing_matches)

        if len(existing_matches) == 0:
            # no existing match: inserting new one
            return self.__db.matches.insert_one(match.toJSON())

        elif len(existing_matches) == 1:
            # existing match: appending odds to existing one
            for odd in match.odds:          
                self.__db.matches.find_and_modify(
                    query,
                    update = {
                        "$push": { "odds" : odd.toJSON() }
                    }
                )

        else:
            raise Exception

    def insert_match_or_update_scores(self, match: Match):

        match_day = datetime.strptime(match.match_date.strftime("%Y-%m-%d"),"%Y-%m-%d")

        query = {
            "bookmaker": match.bookmaker,
            "match_date": {
                "$gte": match_day,
                "$lt": match_day + timedelta(days=1)
                },
            "bookmaker_home_team_id": match.bookmaker_home_team_id,
            "bookmaker_visitor_team_id": match.bookmaker_visitor_team_id,
        }

        existing_matches = self.__db.matches.find(query)
        existing_matches = list(existing_matches)

        if len(existing_matches) == 0:
            # no existing match: inserting new one
            return self.__db.matches.insert_one(match.toJSON())

        elif len(existing_matches) == 1:
            # existing match: updating scores to existing one    
            self.__db.matches.find_and_modify(
                query,
                update = {
                    "$set": {
                        "home_team_score" : match.home_team_score,
                        "visitor_team_score" : match.visitor_team_score
                    }
                }
            )

        else:
            raise Exception

    def dumpDB(self, backup_folder_name: str = ""):
        files = []
        files.append(self.__dumpCollection(self.__db.matches, backup_folder_name))
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

    def dropCollection(self, collection: str):
        self.__db[collection].drop()

    def findMatches(self):
        return self.__db.matches.find({})

    def findMatch(self, date: str, bookmaker: str, bookmaker_home_team_id: int, bookmaker_visitor_team_id: int):

        query = {
            "bookmaker": bookmaker,
            "match_date": {"$gt": date},
            "match_date": {"$lt": date + timedelta(days=1)},
            "bookmaker_home_team_id": bookmaker_home_team_id,
            "bookmaker_visitor_team_id": bookmaker_visitor_team_id,
        }

        return self.__db.matches.find(query)

    def get_last_match_result_date(self):

        query = {
            "home_team_score": { "$ne": None }
        }

        return self.__db.matches.find(query).sort("match_date", -1).limit(1).next().get('match_date')

from pymongo import MongoClient
from bson.json_util import dumps
import sys
import os
import logging

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import MatchResult


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

    def getLastMatchResultDate(self):
        return self.db.match_results.find().sort("date", -1).limit(1).next().get('date')
    
    def dumpDB(self):
        files = []
        files.append(self.dumpCollection(self.db.match_results))
        return files

    def dumpCollection(self, collection) -> str:

        logging.debug("dumping collection '" + collection.full_name + "'")

        cursor = collection.find({})
        with open(collection.full_name + '.json', 'w') as file:
            file.write('[')
            for document in cursor:
                file.write(dumps(document))
                file.write(',')
            file.write(']')

        return collection.full_name + '.json'

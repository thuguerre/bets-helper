from pymongo import MongoClient
import sys
import os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import MatchResult


class BetsMongoDB:

    db = None

    def __init__(self, mongodb_user: str, mongodb_pwd: str, mongodb_name: str):
        client = MongoClient("mongodb+srv://"+mongodb_user+":"+mongodb_pwd+"@cluster0.gu9bi.mongodb.net/"+mongodb_name+"?retryWrites=true&w=majority")
        self.db = client.get_default_database()

    def insertMatchResult(self, match_result: MatchResult):
        return self.db.match_results.insert_one(match_result.toJSON())

    def getLastMatchResultDate(self):
        return self.db.match_results.find().sort("date", -1).limit(1).next().get('date')

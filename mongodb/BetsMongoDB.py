from pymongo import MongoClient
import sys, os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import MatchResult

class BetsMongoDB:

    db = None

    def __init__(self, mongodb_user, mongodb_pwd):
        client = MongoClient("mongodb+srv://"+mongodb_user+":"+mongodb_pwd+"@cluster0.gu9bi.mongodb.net/bets_db?retryWrites=true&w=majority")
        self.db = client.bets_db

    def insertMatchResult(self, match_result: MatchResult):
        return self.db.match_results.insert_one(match_result.toJSON())

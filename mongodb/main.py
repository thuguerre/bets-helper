from decouple import config
from BetsMongoDB import BetsMongoDB

import sys, os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import MatchResult

#
# Main Function
#
if __name__ == '__main__':

    mongodb_user = config('MONGODB_USER')
    mongodb_pwd = config('MONGODB_PWD')
    mongodb_name = config('MONGODB_NAME')

    match_result = MatchResult('2021-06-21', 'baseball', 'japan', 'Regular Season', 'E', 3, 'B', 4)
    bets_db = BetsMongoDB(mongodb_user, mongodb_pwd, mongodb_name)
    result = bets_db.insertMatchResult(match_result)
    print(result.inserted_id)

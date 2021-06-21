from decouple import config
from BetsMongoDB import BetsMongoDB

#
# Main Function
#
if __name__ == '__main__':

    mongodb_user = config('MONGODB_USER')
    mongodb_pwd = config('MONGODB_PWD')

    bets = BetsMongoDB(mongodb_user, mongodb_pwd)
    result = bets.insertJPNBaseBallMatchResult('2021-06-21', 'Regular Season', 'E', 3, 'B', 4)
    print(result.inserted_id)

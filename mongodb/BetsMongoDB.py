from pymongo import MongoClient

class BetsMongoDB:

    db = None

    def __init__(self, mongodb_user, mongodb_pwd):
        client = MongoClient("mongodb+srv://"+mongodb_user+":"+mongodb_pwd+"@cluster0.gu9bi.mongodb.net/bets_db?retryWrites=true&w=majority")
        self.db = client.bets_db

    def insertMatchResult(self, date, sport, country, league, home_team, home_result, visitor_team, visitor_result):

        match_result = {
            'date': date,
            'sport': sport,
            'country': country,
            'league': league,
            'home_team': home_team,
            'home_result': home_result,
            'visitor_team': visitor_team,
            'visitor_result': visitor_result
        }

        return self.db.match_results.insert_one(match_result)

    def insertJPNBaseBallMatchResult(self, date, league, home_team, home_result, visitor_team, visitor_result):
        return self.insertMatchResult(
            date,
            'baseball',
            'japan',
            league,
            home_team,
            home_result,
            visitor_team,
            visitor_result
        )

# Standard Library imports
import os
import pytest
import unittest
from datetime import datetime

# Local imports
import localcontextloader
from mongodb.BetsMongoDB import BetsMongoDB
from betsmodels import MatchResult
from betsmodels import BaseballJapanConverter


class TestUpdateScoresInDb(unittest.TestCase):

    __betsdb: BetsMongoDB = None

    def setUp(self):
        self.__betsdb = BetsMongoDB()
        self.__betsdb.dropCollection('matches')

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_insert_match(self):

        # data case
        date: datetime = datetime.strptime("2021-06-30", "%Y-%m-%d")
        bookmaker = "WINAMAX"
        sport = "baseball"
        country = "japan"
        league = "Regular Season"
        home_team = "T"
        home_score = 3
        visitor_team = "DB"
        visitor_old_score = 4
        visitor_new_score = 5

        converter = BaseballJapanConverter()

        # verifying we start from an empty database        
        self.assertEqual(len(list(self.__betsdb.findMatches())), 0)

        # first insertion in database
        match_result = MatchResult(date.strftime("%Y-%m-%d"), sport, country, league, home_team, home_score, visitor_team, visitor_old_score)
        match_to_insert = match_result.toMatch()
        self.__betsdb.insertMatchOrUpdateScores(match_to_insert)

        # verifying a new match has been inserted
        self.assertEqual(len(list(self.__betsdb.findMatches())), 1)

        # verifying scores are correctly inserted
        matches = list(self.__betsdb.findMatch(date, bookmaker, converter.get_winamax_id(home_team), converter.get_winamax_id(visitor_team)))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["home_team_score"], home_score)
        self.assertEqual(matches[0]["visitor_team_score"], visitor_old_score)

        # updating score in database
        match_result.visitor_score = visitor_new_score
        match_to_update = match_result.toMatch()
        self.__betsdb.insertMatchOrUpdateScores(match_to_update)

        # verifying a new match has not been inserted
        self.assertEqual(len(list(self.__betsdb.findMatches())), 1)

        # verifying the update has been done correctly
        matches = list(self.__betsdb.findMatch(date, bookmaker, converter.get_winamax_id(home_team), converter.get_winamax_id(visitor_team)))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["home_team_score"], home_score)
        self.assertEqual(matches[0]["visitor_team_score"], visitor_new_score)

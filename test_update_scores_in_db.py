# Standard Library imports
import os
import pytest
import unittest
from datetime import datetime
from typing import List

# Local imports
import localcontextloader
from mongodb.BetsMongoDB import BetsMongoDB
from betsmodels import Bookmaker
from betsmodels import Sport
from betsmodels import Country
from betsmodels import Match
from betsmodels import BaseballJapanConverter


class TestUpdateScoresInDb(unittest.TestCase):

    __betsdb: BetsMongoDB = None

    def setUp(self):
        self.__betsdb = BetsMongoDB()
        self.__betsdb.dropCollection('matches')

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_insert_match_or_update_score(self):

        converter = BaseballJapanConverter()

        # data case
        date: datetime = datetime.strptime("2021-06-30", "%Y-%m-%d")
        bookmaker = Bookmaker.WINAMAX
        sport = Sport.BASEBALL
        country = Country.JAPAN
        league = "Regular Season"
        match_id = "-1"
        home_team = "T"
        home_team_name = converter.get_winamax_name(home_team)
        home_team_id = converter.get_winamax_id(home_team)
        home_score = 3
        visitor_team = "DB"
        visitor_team_name = converter.get_winamax_name(visitor_team)
        visitor_team_id = converter.get_winamax_id(visitor_team)
        visitor_old_score = 4
        visitor_new_score = 5

        # verifying we start from an empty database        
        self.assertEqual(len(list(self.__betsdb.findMatches())), 0)

        # first insertion in database
        match_to_insert = Match(date, sport, country, league, date, bookmaker, match_id, home_team_name, home_team_id, home_score, visitor_team_name, visitor_team_id, visitor_old_score)
        self.__betsdb.insert_match_or_update_scores(match_to_insert)

        # verifying a new match has been inserted
        self.assertEqual(len(list(self.__betsdb.findMatches())), 1)

        # verifying scores are correctly inserted
        matches = list(self.__betsdb.findMatch(date, bookmaker, converter.get_winamax_id(home_team), converter.get_winamax_id(visitor_team)))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["home_team_score"], home_score)
        self.assertEqual(matches[0]["visitor_team_score"], visitor_old_score)

        # updating score in database
        match_to_insert.visitor_team_score = visitor_new_score
        self.__betsdb.insert_match_or_update_scores(match_to_insert)

        # verifying a new match has not been inserted
        self.assertEqual(len(list(self.__betsdb.findMatches())), 1)

        # verifying the update has been done correctly
        matches = list(self.__betsdb.findMatch(date, bookmaker, converter.get_winamax_id(home_team), converter.get_winamax_id(visitor_team)))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["home_team_score"], home_score)
        self.assertEqual(matches[0]["visitor_team_score"], visitor_new_score)

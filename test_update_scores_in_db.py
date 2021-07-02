# Standard Library imports
import os
import pytest
import unittest

# Local imports
import localcontextloader
from mongodb.BetsMongoDB import BetsMongoDB
from betsmodels import MatchResult


class TestUpdateScoresInDb(unittest.TestCase):

    __betsdb: BetsMongoDB = None

    def setUp(self):
        self.__betsdb = BetsMongoDB()
        self.__betsdb.dropCollection('matches')
        self.assertEqual(len(list(self.__betsdb.findMatches())), 0)

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_insert_match(self):
        
        match_result = MatchResult("2021-06-30", "baseball", "japan", "Regular Season", "T", 3, "DB", 4)
        match_to_insert = match_result.toMatch()
        self.__betsdb.insertMatchOrAppendOdds(match_to_insert)

        self.assertEqual(len(list(self.__betsdb.findMatches())), 1)

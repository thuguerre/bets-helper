# Standard Library imports
import pytest
import unittest
from datetime import datetime
import logging

# Local imports
import localcontextloader
from betsmodels import MatchResult
from mongodb.BetsMongoDB import BetsMongoDB

class TestGetLastMatchResultDate(unittest.TestCase):

    __betsdb = None

    def setUp(self):
        self.__betsdb = BetsMongoDB()
        self.__betsdb.dropCollection('matches')
        
    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_get_date(self):

        # verifying we start from an empty database        
        self.assertEqual(len(list(self.__betsdb.findMatches())), 0)

        # filling database with a known data case
        data = [
            MatchResult("2020-06-30", "baseball", "japan", "Regular Season", "T", 1, "C", 2),
            MatchResult("2020-06-30", "baseball", "japan", "Regular Season", "DB", 5, "F", 4),
            MatchResult("2020-07-01", "baseball", "japan", "Regular Season", "T", 1, "C", 2),
            MatchResult("2020-07-01", "baseball", "japan", "Regular Season", "DB", 1, "F", 2),
            MatchResult("2020-07-02", "baseball", "japan", "Regular Season", "G", None, "M", None),
        ]

        for match_result in data:
            self.__betsdb.insert_match_or_update_scores(match_result.toMatch())

        # verifying match results have been correctly inserted
        self.assertEqual(len(list(self.__betsdb.findMatches())), len(data))

        # getting last match result's date
        last_date = self.__betsdb.get_last_match_result_date()
        last_date = datetime.strftime(last_date, '%Y-%m-%d')
        self.assertEqual(last_date, '2020-07-01')

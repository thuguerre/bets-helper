import pytest
import unittest
import os
from LocalExecHelper import LocalExecHelper
# from mongodb.BetsMongoDB import BetsMongoDB


class TestUpdateScoresInDb(unittest.TestCase):

    mongodb: BetsMongoDB = None

    def setUp(self):

        try:
            os.environ["MONGODB_NAME"]
        except KeyError:
            LocalExecHelper()

        #self.mongodb = BetsMongoDB()
        #self.mongodb.matches.drop()

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_insert_match(self):
        
        #match_result = MatchResult("2021-06-30", "baseball", "japan", "Regular Season", "T", 3, "DB", 4)
        #match_to_insert = match_result.toMatch()
        #self.mongodb.insertMatchOrAppendOdds(match_to_insert)

        # self.assertEqual(len(self.mongodb.matches.find({})), 1)
        pass


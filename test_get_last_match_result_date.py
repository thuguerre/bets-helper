# Standard Library imports
import pytest
import unittest
from datetime import datetime
import logging

# Local imports
import localcontextloader
from betsmodels import Match
from betsmodels import Country
from betsmodels import Bookmaker
from betsmodels import Sport
from betsmodels import BaseballJapanConverter
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
        converter = BaseballJapanConverter()
        data = [
            Match(
                datetime.strptime("2021-06-30", "%Y-%m-%d"),
                Sport.BASEBALL,
                Country.JAPAN,
                "Regular Season",
                datetime.strptime("2021-06-30", "%Y-%m-%d"),
                Bookmaker.WINAMAX,
                "-1",
                converter.get_winamax_name("T"),
                converter.get_winamax_id("T"),
                1,
                converter.get_winamax_name("C"),
                converter.get_winamax_id("C"),
                2
            ),
            Match(
                datetime.strptime("2021-06-30", "%Y-%m-%d"),
                Sport.BASEBALL,
                Country.JAPAN,
                "Regular Season",
                datetime.strptime("2021-06-30", "%Y-%m-%d"),
                Bookmaker.WINAMAX, "-1",
                converter.get_winamax_name("DB"),
                converter.get_winamax_id("DB"),
                5,
                converter.get_winamax_name("F"),
                converter.get_winamax_id("F"),
                4
            ),
            Match(
                datetime.strptime("2021-07-01", "%Y-%m-%d"),
                Sport.BASEBALL,
                Country.JAPAN,
                "Regular Season",
                datetime.strptime("2021-07-01", "%Y-%m-%d"),
                Bookmaker.WINAMAX, "-1",
                converter.get_winamax_name("T"),
                converter.get_winamax_id("T"),
                1,
                converter.get_winamax_name("C"),
                converter.get_winamax_id("C"),
                2
            ),
            Match(
                datetime.strptime("2021-07-01", "%Y-%m-%d"),
                Sport.BASEBALL,
                Country.JAPAN,
                "Regular Season",
                datetime.strptime("2021-07-01", "%Y-%m-%d"),
                Bookmaker.WINAMAX, "-1",
                converter.get_winamax_name("DB"),
                converter.get_winamax_id("DB"),
                1,
                converter.get_winamax_name("F"),
                converter.get_winamax_id("F"),
                2
            ),
            Match(
                datetime.strptime("2021-07-02", "%Y-%m-%d"),
                Sport.BASEBALL,
                Country.JAPAN,
                "Regular Season",
                datetime.strptime("2021-07-02", "%Y-%m-%d"),
                Bookmaker.WINAMAX, "-1",
                converter.get_winamax_name("G"),
                converter.get_winamax_id("G"),
                None,
                converter.get_winamax_name("M"),
                converter.get_winamax_id("M"),
                None
            )
        ]

        for match in data:
            self.__betsdb.insert_match_or_update_scores(match)

        # verifying match results have been correctly inserted
        self.assertEqual(len(list(self.__betsdb.findMatches())), len(data))

        # getting last match result's date
        last_date = self.__betsdb.get_last_match_result_date()
        last_date = datetime.strftime(last_date, '%Y-%m-%d')
        self.assertEqual(last_date, '2021-07-01')

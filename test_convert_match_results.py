# Standard Library imports
import pytest
import unittest

# Local imports
from betsmodels import BaseballJapanConverter, MatchResult


class TestConvertMatchResultsToMatch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_converter(self):
        
        converter = BaseballJapanConverter()

        self.assertEqual(converter.get_winamax_name("T"), "Hanshin Tigers")
        self.assertEqual(converter.get_winamax_id("T"), 22108)

        self.assertEqual(converter.get_winamax_name("DB"), "Yokohama Baystars")
        self.assertEqual(converter.get_winamax_id("DB"), 67110)

    @pytest.mark.unittest
    def test_convertion_match_result_to_match(self):

        match_result = MatchResult("2021-06-30", "baseball", "japan", "Regular Season", "T", 3, "DB", 4)

        match = match_result.toMatch()

        self.assertEqual(str(match.timestamp), "2021-06-30 00:00:00")
        self.assertEqual(match.sport, "BASEBALL")
        self.assertEqual(match.country, "JAPAN")
        self.assertEqual(match.league, "Regular Season")
        self.assertEqual(str(match.match_date), "2021-06-30 00:00:00")
        self.assertEqual(match.bookmaker, "WINAMAX")
        self.assertEqual(match.bookmaker_match_id, "-1")
        self.assertEqual(match.bookmaker_home_team_name, "Hanshin Tigers")
        self.assertEqual(match.bookmaker_home_team_id, 22108)
        self.assertEqual(match.bookmaker_visitor_team_name, "Yokohama Baystars")
        self.assertEqual(match.bookmaker_visitor_team_id, 67110)
        self.assertEqual(match.home_team_score, 3)
        self.assertEqual(match.visitor_team_score, 4)

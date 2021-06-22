import pytest, unittest
from betsmodels import MatchResult

class TestBetsModels(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_to_json(self):
        date = '2021-06-22'
        sport = 'baseball'
        country = 'japan'
        league = 'Regular Season'
        home_team = 'C'
        home_score = 1
        visitor_team = 'F'
        visitor_score = 8

        match_result = MatchResult(date, sport, country, league, home_team, home_score, visitor_team, visitor_score)

        self.assertEqual(
            match_result.toJSON(),
            {
                "date": date,
                "sport": sport,
                "country": country,
                "league": league,
                "home_team": home_team,
                "home_score": home_score,
                "visitor_team": visitor_team,
                "visitor_score": visitor_score
            }
        )


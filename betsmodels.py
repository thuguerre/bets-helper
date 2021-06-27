import datetime
from enum import Enum
from typing import List


class MatchResult:

    date = None
    sport = None
    country = None
    league = None
    home_team = None
    home_score = None
    visitor_team = None
    vistor_score = None

    def __init__(self, date: str, sport: str, country: str, league: str, home_team: str, home_score: int, visitor_team: str, visitor_score: int):
        self.date = date
        self.sport = sport
        self.country = country
        self.league = league
        self.home_team = home_team
        self.home_score = home_score
        self.visitor_team = visitor_team
        self.visitor_score = visitor_score

    def toJSON(self) -> dict:
        return {
            "date": self.date,
            "sport": self.sport,
            "country": self.country,
            "league": self.league,
            "home_team": self.home_team,
            "home_score": self.home_score,
            "visitor_team": self.visitor_team,
            "visitor_score": self.visitor_score
        }

    def toMongoDBDataFragment(self) -> str:
        return (
            "\"date\": \"" + self.date + "\""
            + ", \"sport\": \"" + self.sport + "\""
            + ", \"country\": \"" + self.country + "\""
            + ", \"league\": \"" + self.league + "\""
            + ", \"home_team\": \"" + self.home_team + "\""
            + ", \"home_score\": \"" + self.home_score + "\""
            + ", \"visitor_team\": \"" + self.visitor_team + "\""
            + ", \"visitor_score\": \"" + self.visitor_score + "\""
        )

class OddType(Enum):
    RESULT = 1  # team 1 winner, draw or team 2 winner

    SCORE_GT_0_5 = 10
    SCORE_GT_1_5 = 11
    SCORE_GT_2_5 = 12
    SCORE_GT_3_5 = 13
    SCORE_GT_4_5 = 14
    SCORE_GT_5_5 = 15
    SCORE_GT_6_5 = 16
    SCORE_GT_7_5 = 17
    SCORE_GT_8_5 = 18
    SCORE_GT_9_5 = 19
    SCORE_GT_10_5 = 20
    SCORE_GT_11_5 = 21
    SCORE_GT_12_5 = 22
    SCORE_GT_13_5 = 23
    SCORE_GT_14_5 = 24

    SCORE_LT_0_5 = 30
    SCORE_LT_1_5 = 31
    SCORE_LT_2_5 = 32
    SCORE_LT_3_5 = 33
    SCORE_LT_4_5 = 34
    SCORE_LT_5_5 = 35
    SCORE_LT_6_5 = 36
    SCORE_LT_7_5 = 37
    SCORE_LT_8_5 = 38
    SCORE_LT_9_5 = 39
    SCORE_LT_10_5 = 40
    SCORE_LT_11_5 = 41
    SCORE_LT_12_5 = 42
    SCORE_LT_13_5 = 43
    SCORE_LT_14_5 = 44

class OddStatus(Enum):
    PREMATCH = 1

class Bookmaker(Enum):
    WINAMAX = 1

class Sport(Enum):
    BASEBALL = 1

class Country(Enum):
    JAPAN = 1

class Odd:

    timestamp: datetime = None  # timestamp when odd has been retrieved

    odd_status: OddStatus = None
    odd_type: OddType = None
    odd_target: str = None
    odd_value: float = None

    def __init__(self, timestamp: datetime, odd_status: OddStatus, odd_type: OddType, odd_target: str, odd_value: float):
        self.timestamp = timestamp
        self.odd_status = odd_status
        self.odd_type = odd_type
        self.odd_target = odd_target
        self.odd_value = odd_value

    def toJSON(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "odd_status": self.odd_status,
            "odd_type": self.odd_type,
            "odd_target": self.odd_target,
            "odd_value": self.odd_value
        }

class Match:

    timestamp: datetime = None  # timestamp when this match has been created
    
    sport: Sport = None
    country: Country = None
    league: str = None
    match_date: datetime = None

    bookmaker: Bookmaker = None
    bookmaker_match_id: str = None
    bookmaker_home_team_name: str = None
    bookmaker_home_team_id: str = None
    bookmaker_visitor_team_name: str = None
    bookmaker_visitor_team_id: str = None

    odds: List[Odd] = []

    def __init__(self, timestamp: datetime, sport: Sport, country: Country, league: str, match_date: datetime, bookmaker: Bookmaker, bookmaker_match_id: str, bookmaker_home_team_name: str, bookmaker_home_team_id: str, bookmaker_visitor_team_name: str, bookmaker_visitor_team_id: str):
        self.timestamp = timestamp
        self.sport = sport
        self.country = country
        self.league = league
        self.match_date = match_date
        self.bookmaker = bookmaker
        self.bookmaker_match_id = bookmaker_match_id
        self.bookmaker_home_team_name = bookmaker_home_team_name
        self.bookmaker_home_team_id = bookmaker_home_team_id
        self.bookmaker_visitor_team_name = bookmaker_visitor_team_name
        self.bookmaker_visitor_team_id = bookmaker_visitor_team_id

    def toJSON(self) -> dict:
        result = {
            "timestamp": self.timestamp,
            "sport": self.sport,
            "country": self.country,
            "league": self.league,
            "match_date": self.match_date,
            "bookmaker": self.bookmaker,
            "bookmaker_match_id": self.bookmaker_match_id,
            "bookmaker_home_team_name": self.bookmaker_home_team_name,
            "bookmaker_home_team_id": self.bookmaker_home_team_id,
            "bookmaker_visitor_team_name": self.bookmaker_visitor_team_name,
            "bookmaker_visitor_team_id": self.bookmaker_visitor_team_id,
            "odds": []
        }
        return result

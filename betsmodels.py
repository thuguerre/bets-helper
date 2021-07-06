# Standard Library imports
import datetime
from enum import Enum
from typing import List


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
    LIVE = 2

class Bookmaker(Enum):
    WINAMAX = 1

class Sport(Enum):
    BASEBALL = 1

class Country(Enum):
    JAPAN = 1

class Odd:

    timestamp: datetime = None  # timestamp when odd has been retrieved

    odd_status: str = None
    odd_type: str = None
    odd_target: str = None
    odd_value: float = None

    def __init__(self, timestamp: datetime, odd_status: OddStatus, odd_type: OddType, odd_target: str, odd_value: float):
        self.timestamp = timestamp
        self.odd_status = odd_status.name
        self.odd_type = odd_type.name
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
    
    sport: str = None
    country: str = None
    league: str = None
    match_date: datetime = None

    bookmaker: str = None
    bookmaker_match_id: str = None
    bookmaker_home_team_name: str = None
    bookmaker_home_team_id: str = None
    bookmaker_visitor_team_name: str = None
    bookmaker_visitor_team_id: str = None

    home_team_score: int = None
    visitor_team_score: int = None

    odds: List[Odd] = []

    def __init__(self, timestamp: datetime, sport: Sport, country: Country, league: str, match_date: datetime, bookmaker: Bookmaker, bookmaker_match_id: str, bookmaker_home_team_name: str, bookmaker_home_team_id: str, home_team_score: int, bookmaker_visitor_team_name: str, bookmaker_visitor_team_id: str, visitor_team_score: int):
        self.timestamp = timestamp
        self.sport = sport.name
        self.country = country.name
        self.league = league
        self.match_date = match_date
        self.bookmaker = bookmaker.name if bookmaker != None else None
        self.bookmaker_match_id = bookmaker_match_id
        self.bookmaker_home_team_name = bookmaker_home_team_name
        self.bookmaker_home_team_id = bookmaker_home_team_id
        self.bookmaker_visitor_team_name = bookmaker_visitor_team_name
        self.bookmaker_visitor_team_id = bookmaker_visitor_team_id
        self.home_team_score = home_team_score
        self.visitor_team_score = visitor_team_score
        self.odds = []

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
            "home_team_score": self.home_team_score,
            "visitor_team_score": self.visitor_team_score,
            "odds": []
        }
        for odd in self.odds:
            result["odds"].append(odd.toJSON())
        return result

    def toMongoDBDataFragment(self) -> str:
        return (
            f"\"bookmaker\": \"{self.bookmaker}\""
            + f", \"bookmaker_match_id\": \"{self.bookmaker_match_id}\""
            + f", \"bookmaker_home_team_name\": \"{self.bookmaker_home_team_name}\""
            + f", \"bookmaker_home_team_id\": \"{self.bookmaker_home_team_id}\""
            + f", \"bookmaker_visitor_team_name\": \"{self.bookmaker_visitor_team_name}\""
            + f", \"bookmaker_visitor_team_id\": \"{self.bookmaker_visitor_team_id}\""
        )

class BaseballJapanConverter:

    references = [
        {"nbp_letter": "B", "winamax_name": "Orix Buffaloes", "winamax_id": 67116},
        {"nbp_letter": "C", "winamax_name": "Hiroshima Toyo Carp", "winamax_id": 67106},
        {"nbp_letter": "D", "winamax_name": "Chunichi Dragons", "winamax_id": 67104},
        {"nbp_letter": "DB", "winamax_name": "Yokohama Baystars", "winamax_id": 67110},
        {"nbp_letter": "E", "winamax_name": "Rakuten Gold. Eagles", "winamax_id": 67118},
        {"nbp_letter": "F", "winamax_name": "Hokkaido Nippon-Ham Fighters", "winamax_id": 67114},
        {"nbp_letter": "G", "winamax_name": "Yomiuri Giants", "winamax_id": 34374},
        {"nbp_letter": "H", "winamax_name": "Fukuoka Softbank Hawks", "winamax_id": 67122},
        {"nbp_letter": "L", "winamax_name": "Saitama Seibu Lions", "winamax_id": 67120},
        {"nbp_letter": "M", "winamax_name": "Chiba Lotte Marines", "winamax_id": 67112},
        {"nbp_letter": "S", "winamax_name": "Tokyo Yakult Swallows", "winamax_id": 67108},
        {"nbp_letter": "T", "winamax_name": "Hanshin Tigers", "winamax_id": 22108}
    ]

    def get_winamax_name(self, npb_letter: str) -> str:
        for reference in self.references:
            if reference["nbp_letter"] == npb_letter:
                return reference["winamax_name"]

        raise Exception

    def get_winamax_id(self, npb_letter: str) -> int:
        for reference in self.references:
            if reference["nbp_letter"] == npb_letter:
                return reference["winamax_id"]

        raise Exception
        
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
            f"\"date\": \"{self.date}\""
            + f", \"sport\": \"{self.sport}\""
            + f", \"country\": \"{self.country}\""
            + f", \"league\": \"{self.league}\""
            + f", \"home_team\": \"{self.home_team}\""
            + f", \"home_score\": \"{self.home_score}\""
            + f", \"visitor_team\": \"{self.visitor_team}\""
            + f", \"visitor_score\": \"{self.visitor_score}\""
        )

    def toMatch(self) -> Match:

        converter = BaseballJapanConverter()

        mTimestamp: datetime = datetime.datetime.strptime(self.date,"%Y-%m-%d")

        mSport: Sport = None
        if self.sport == "baseball":
            mSport = Sport.BASEBALL
        else:
            raise Exception

        mCountry: Country = None
        if self.country == "japan":
            mCountry = Country.JAPAN
        else:
            raise Exception

        mLeague: str = self.league
        mMatch_date: datetime = datetime.datetime.strptime(self.date,"%Y-%m-%d")
        mBookmaker: Bookmaker = Bookmaker.WINAMAX
        mBookmaker_match_id: str = "-1"
        mBookmaker_home_team_name: str = converter.get_winamax_name(self.home_team)
        mBookmaker_home_team_id: str = converter.get_winamax_id(self.home_team)
        mBookmaker_visitor_team_name: str = converter.get_winamax_name(self.visitor_team)
        mBookmaker_visitor_team_id: str = converter.get_winamax_id(self.visitor_team)
        
        match = Match(
            mTimestamp,
            mSport,
            mCountry,
            mLeague,
            mMatch_date,
            mBookmaker,
            mBookmaker_match_id,
            mBookmaker_home_team_name,
            mBookmaker_home_team_id,
            self.home_score,
            mBookmaker_visitor_team_name,
            mBookmaker_visitor_team_id,
            self.visitor_score
        )

        return match

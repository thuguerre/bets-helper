import ssl
import requests
import re
from urllib3 import poolmanager
import json
from datetime import datetime
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import Match
from betsmodels import Odd
from betsmodels import Sport
from betsmodels import Country
from betsmodels import OddStatus
from betsmodels import OddType
from betsmodels import Bookmaker

from mongodb.BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper

URL_BASEBALL_JAPAN_HOMEPAGE = "https://www.winamax.fr/paris-sportifs/sports/3/211"
WINAMAX_SPORT_ID_BASEBALL = 3   # normally 3
WINAMAX_SPORT_CATEGORY_ID_BASEBALL_JAPAN = 211 # normally 211

# Adapter to prevent SSL Signature error while getting NPB web site content
# https://github.com/psf/requests/issues/4775
class TLSAdapter(requests.adapters.HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLS,
                ssl_context=ctx)


class ParseException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class WinamaxCrawler:

    def retrieve_odds(self):

        session = requests.session()
        session.mount('https://', TLSAdapter())
        homepage = session.get(URL_BASEBALL_JAPAN_HOMEPAGE)

        self.__loads_PRELOADED_STATE(homepage.text)
        
    def __loads_PRELOADED_STATE(self, homepage_text: str):

        allscripts_regex = re.compile('<script type="text/javascript">(.*)</script><script type="text/javascript">var BETTING_CONFIGURATION =')
        allscripts = allscripts_regex.findall(homepage_text)

        if len(allscripts) != 1:
            raise ParseException
        
        json_raw = allscripts[0].replace("var PRELOADED_STATE = ", "")
        json_raw = json_raw[0:len(json_raw) - 1] # remove last ;
        PRELOADED_STATE = json.loads(json_raw)

        for match_id in PRELOADED_STATE["matches"]:
            match = PRELOADED_STATE["matches"][match_id]
            if match["sportId"] == WINAMAX_SPORT_ID_BASEBALL and match["categoryId"] == WINAMAX_SPORT_CATEGORY_ID_BASEBALL_JAPAN:
                
                retrieved_match = Match(datetime.now(), Sport.BASEBALL, Country.JAPAN, "Regular Season", datetime.fromtimestamp(match["matchStart"]), Bookmaker.WINAMAX, match["matchId"], match["competitor1Name"], match["competitor1Id"], match["competitor2Name"], match["competitor2Id"])
                
                if match["status"] == 'PREMATCH':
                    oddStatus = OddStatus.PREMATCH
                else:
                    raise ParseException

                mainBet = PRELOADED_STATE["bets"][str(match["mainBetId"])]

                odd1 = Odd(datetime.now(), oddStatus, OddType.RESULT, match["competitor1Id"], PRELOADED_STATE["odds"][str(mainBet["outcomes"][0])])
                odd2 = Odd(datetime.now(), oddStatus, OddType.RESULT, match["competitor2Id"], PRELOADED_STATE["odds"][str(mainBet["outcomes"][1])])
                
                retrieved_match.odds.append(odd1)
                retrieved_match.odds.append(odd2)

                print(retrieved_match.toJSON())

                LocalExecHelper()
                mongodb = BetsMongoDB()
                mongodb.insertMatch(retrieved_match)

        

        


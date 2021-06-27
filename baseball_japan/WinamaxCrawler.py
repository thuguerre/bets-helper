import ssl
import requests
import re
from urllib3 import poolmanager
import json


URL_BASEBALL_JAPAN_HOMEPAGE = "https://www.winamax.fr/paris-sportifs/sports/3/211"

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

    odds = {}

    def test(self):

        session = requests.session()
        session.mount('https://', TLSAdapter())
        homepage = session.get(URL_BASEBALL_JAPAN_HOMEPAGE)

        

        #allmatches_regex = re.compile('\"title\":\"[a-zA-Z \-]*\",')
        #allmatches = allmatches_regex.findall(homepage.text)
        #for onematch in allmatches:
        #    print(onematch)

        self.__loads_PRELOADED_STATE(homepage.text)
        self.__loads_odds(homepage.text)
        # print(self.odds["399024240"])
        
    def __loads_PRELOADED_STATE(self, homepage_text: str):

        allscripts_regex = re.compile('<script type="text/javascript">(.*)</script><script type="text/javascript">var BETTING_CONFIGURATION =')
        allscripts = allscripts_regex.findall(homepage_text)

        if len(allscripts) != 1:
            raise ParseException
        
        json_raw = allscripts[0].replace("var PRELOADED_STATE = ", "")
        json_raw = json_raw[0:len(json_raw) - 1]
        PRELOADED_STATE = json.loads(json_raw)

        for sportId in PRELOADED_STATE["sportIds"]:
            print(sportId)
    
    def __loads_odds(self, homepage_text: str):

        allodds_regex = re.compile('\"odds\":{[0-9\":.,]*},')
        allodds = allodds_regex.findall(homepage_text)

        if len(allodds) != 1:
            raise ParseException
        
        self.odds = json.loads(allodds[0][7:len(allodds[0])-1])


        

        


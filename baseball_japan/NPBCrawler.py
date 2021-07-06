# Standard Library imports
import os
import sys
import logging
import requests
import ssl
import re
from urllib3 import poolmanager
from datetime import datetime

# Local imports
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from betsmodels import Match
from betsmodels import BaseballJapanConverter
from betsmodels import Sport
from betsmodels import Country


URL_Farm_Leagues = "https://npb.jp/bis/eng/<YEAR>/calendar/index_farm_<MONTH>.html"
URL_Regular_Season = "https://npb.jp/bis/eng/<YEAR>/calendar/index_<MONTH>.html"


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


class NPBCrawler:

    def retrieve_month_results(self, year_to_get, month_to_get, league_to_get, from_day, to_day):

        if len(month_to_get) == 1:
            month_to_get = "0" + month_to_get

        logging.debug("retrieving '" + league_to_get + "' results for " + year_to_get + "-" + month_to_get)
        logging.debug("from_day : " + str(from_day))
        logging.debug("to_day : " + str(to_day))

        if league_to_get == 'Farm Leagues':
            url = URL_Farm_Leagues.replace('<YEAR>', year_to_get).replace('<MONTH>', month_to_get)
            day_regex = re.compile('<a href="/bis/eng/'+year_to_get+'/games/fs([0-9]{8})')

        elif league_to_get == 'Regular Season':
            url = URL_Regular_Season.replace('<YEAR>', year_to_get).replace('<MONTH>', month_to_get)
            day_regex = re.compile('<a href="/bis/eng/'+year_to_get+'/games/s([0-9]{8})')

        # getting HTML page content to then parse
        logging.debug(url)
        session = requests.session()
        session.mount('https://', TLSAdapter())
        wholepage = session.get(url)

        allmatches_regex = re.compile('<a href="[a-zA-Z0-9\.\/]*">[A-Z]{1,2} [0-9*]{1,3} - [0-9*]{1,2} [A-Z]{1,2}')
        matchresult_regex = re.compile('([A-Z]{1,2} [0-9*]{1,3} - [0-9*]{1,2} [A-Z]{1,2})')

        allmatches = allmatches_regex.findall(wholepage.text)

        month_results = []

        for onematch in allmatches:
            match_day = day_regex.search(onematch).group(1)
            match_result = matchresult_regex.search(onematch).group(1)

            add_match = True

            if from_day > 0 and from_day > int(match_day[6:9]):
                add_match = False

            if to_day > 0 and to_day < int(match_day[6:9]):
                add_match = False

            if add_match:
                converter = BaseballJapanConverter()
                match_result_to_add = Match(
                    datetime.strptime(match_day, "%Y%m%d"),
                    Sport.BASEBALL,
                    Country.JAPAN,
                    league_to_get,
                    datetime.strptime(match_day, "%Y%m%d"),
                    None,
                    "-1",
                    converter.get_winamax_name(match_result.split()[0]),
                    converter.get_winamax_id(match_result.split()[0]),
                    match_result.split()[1],
                    converter.get_winamax_name(match_result.split()[4]),
                    converter.get_winamax_id(match_result.split()[4]),
                    match_result.split()[3]
                )
                logging.info(match_result_to_add.toJSON())
                month_results.append(match_result_to_add)

        return month_results

    def retrieve_results(self, start_year, start_month, start_day, to_year, to_month, to_day, league_to_get):

        logging.info("retrieve results from:" + start_year + "-" + start_month + "-" + start_day + " to " + to_year + "-" + to_month + "-" + to_day)

        current_year = int(start_year)
        current_month = int(start_month)

        results = []

        increment_month = True
        while increment_month:

            local_from_day = 0
            local_to_day = 0

            if current_year == int(start_year) and current_month == int(start_month):
                local_from_day = int(start_day)

            if current_year == int(to_year) and current_month == int(to_month):
                local_to_day = int(to_day)

            month_results = self.retrieve_month_results(str(current_year), str(current_month), league_to_get, local_from_day, local_to_day)
            for month_result in month_results:
                results.append(month_result)

            if current_year < int(to_year):
                current_month += 1
                if current_month == 13:
                    current_year += 1
                    current_month = 1
            elif current_year == int(to_year) and current_month < int(to_month):
                current_month += 1
            elif current_year == int(to_year) and current_month == int(to_month):
                increment_month = False
            else:
                raise "Should not be in this case"

        return results

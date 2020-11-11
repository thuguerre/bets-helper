import requests
import re
import sys
from datetime import date
import logging

URL_Farm_Leagues = "https://npb.jp/bis/eng/<YEAR>/calendar/index_farm_<MONTH>.html"
URL_Regular_Season = "https://npb.jp/bis/eng/<YEAR>/calendar/index_<MONTH>.html"

def retrieve_month_results(year_to_get, month_to_get, league_to_get, from_day, to_day):

    if len(month_to_get) == 1:
        month_to_get = "0" + month_to_get

    logging.debug("retrieving '" + league_to_get + "' results for " + year_to_get + "-" + month_to_get)
    logging.debug("from_day : " + str(from_day))
    logging.debug("to_day : " + str(to_day))

    if league_to_get == 'Farm Leagues':
        url = URL_Farm_Leagues.replace('<YEAR>', year_to_get).replace('<MONTH>', month_to_get)
        day_regex = re.compile('<a href="/bis/eng/2020/games/fs([0-9]{8})')

    elif league_to_get == 'Regular Season': 
        url = URL_Regular_Season.replace('<YEAR>', year_to_get).replace('<MONTH>', month_to_get)
        day_regex = re.compile('<a href="/bis/eng/2020/games/s([0-9]{8})')

    logging.debug(url)
    wholepage = requests.get(url)

    allmatches_regex = re.compile('<a href="[a-zA-Z0-9\.\/]*">[A-Z] [0-9*]{1,3} - [0-9*]{1,2} [A-Z]')
    matchresult_regex = re.compile('([A-Z] [0-9*]{1,3} - [0-9*]{1,2} [A-Z])')

    allmatches = allmatches_regex.findall(wholepage.text)

    for onematch in allmatches:
        match_day = day_regex.search(onematch).group(1)
        match_result = matchresult_regex.search(onematch).group(1)

        print_match = True
        
        if from_day > 0 and from_day > int(match_day[6:9]):
            print_match = False

        if to_day > 0 and to_day < int(match_day[6:9]):
            print_match = False

        if print_match:
            print(match_day[0:4] + "-" + match_day[4:6] + "-" + match_day[6:9] + "\t\t" + league_to_get + "\t\t\t " + match_result)


def retrieve_results(start_year, start_month, start_day, to_year, to_month, to_day, league_to_get):

    logging.info("retrieve results from:" + start_year + "-" + start_month + "-" + start_day + " to " + to_year + "-" + to_month + "-" + to_day)

    current_year = int(start_year)
    current_month = int(start_month)

    increment_month = True
    while increment_month:
        
        local_from_day = 0
        local_to_day = 0

        if current_year == int(start_year) and current_month == int(start_month):
            local_from_day = int(start_day)

        if current_year == int(to_year) and current_month == int(to_month):
            local_to_day = int(to_day)

        retrieve_month_results(str(current_year), str(current_month), league_to_get, local_from_day, local_to_day)

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

#
# Documentation Printing Method
#
def printDocumentation():

    print("args 'from:YYYYMMDD'. If not set, from current year and month.")
    print("args 'to:YYYYMMDD'. If not set, current year, month and day.")

#
# Main Function
#
if __name__ == '__main__':
    
    logging.getLogger().setLevel(logging.WARN)

    today = date.today()

    start_year = today.strftime("%Y")
    start_month = today.strftime("%m")
    start_day = today.strftime("%d")

    to_year = today.strftime("%Y")
    to_month = today.strftime("%m")
    to_day = today.strftime("%d")

    for args in sys.argv:

        if args.startswith("from:"):
            start_year = args[5:9]
            start_month = args[9:11]
            start_day = args[11:13]

        elif args.startswith("to:"):
            to_year = args[3:7]
            to_month = args[7:9]
            to_day = args[9:11]

        elif args == '-h' or args == "-help" or args == "--h" or args == "--help":
            printDocumentation()
            sys.exit()

    if int(start_year) > int(to_year):
        logging.error("retrieve results from:" + start_year + "-" + start_month + "-" + start_day + " to " + to_year + "-" + to_month + "-" + to_day)
        logging.error("FROM year cannnot be greater than TO year")
        sys.exit()
    elif int(start_year) == int(to_year) and int(start_month) > int(to_month):
        logging.error("retrieve results from:" + start_year + "-" + start_month + "-" + start_day + " to " + to_year + "-" + to_month + "-" + to_day)
        logging.error("FROM month cannnot be greater than TO month")
        sys.exit()
    elif int(start_year) == int(to_year) and int(start_month) == int(to_month) and int(start_day) > int(to_day):
        logging.error("retrieve results from:" + start_year + "-" + start_month + "-" + start_day + " to " + to_year + "-" + to_month + "-" + to_day)
        logging.error("FROM day cannnot be greater than TO day")
        sys.exit()

    retrieve_results(start_year, start_month, start_day, to_year, to_month, to_day, 'Regular Season')
    


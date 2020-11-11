import requests
import re
import sys
from datetime import date

URL_Farm_Leagues = "https://npb.jp/bis/eng/<YEAR>/calendar/index_farm_<MONTH>.html"
URL_Regular_Season = "https://npb.jp/bis/eng/<YEAR>/calendar/index_<MONTH>.html"

def retrieve_results(year_to_get, month_to_get, league_to_get):

    if len(month_to_get) == 1:
        month_to_get = "0" + month_to_get

    if league_to_get == 'Farm Leagues':
        url = URL_Farm_Leagues.replace('<YEAR>', year_to_get).replace('<MONTH>', month_to_get)
        day_regex = re.compile('<a href="/bis/eng/2020/games/fs([0-9]{8})')

    elif league_to_get == 'Regular Season': 
        url = URL_Regular_Season.replace('<YEAR>', year_to_get).replace('<MONTH>', month_to_get)
        day_regex = re.compile('<a href="/bis/eng/2020/games/s([0-9]{8})')

    print(url)
    wholepage = requests.get(url)

    allmatches_regex = re.compile('<a href="[a-zA-Z0-9\.\/]*">[A-Z] [0-9*]{1,3} - [0-9*]{1,2} [A-Z]')
    matchresult_regex = re.compile('([A-Z] [0-9*]{1,3} - [0-9*]{1,2} [A-Z])')

    allmatches = allmatches_regex.findall(wholepage.text)

    for onematch in allmatches:
        day = day_regex.search(onematch).group(1)
        result = matchresult_regex.search(onematch).group(1)

        print(day[0:4] + "-" + day[4:6] + "-" + day[6:9] + "\t\t" + league_to_get + "\t\t\t " + result)

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
            start_year = args[3:7]
            start_month = args[7:9]
            start_day = args[9:11]

        elif args == '-h' or args == "-help" or args == "--h" or args == "--help":
            printDocumentation()
            sys.exit()

    print("retrieve result from:" + start_year + "-" + start_month + "-" + start_day + " to " + to_year + "-" + to_month + "-" + to_day)

    current_year = int(start_year)
    current_month = int(start_month)

    increment_month = True
    while increment_month:
        
        retrieve_results(str(current_year), str(current_month), 'Regular Season')

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


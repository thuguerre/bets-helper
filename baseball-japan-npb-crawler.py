import requests
import re
import sys
import os
from datetime import date, timedelta
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

URL_Farm_Leagues = "https://npb.jp/bis/eng/<YEAR>/calendar/index_farm_<MONTH>.html"
URL_Regular_Season = "https://npb.jp/bis/eng/<YEAR>/calendar/index_<MONTH>.html"

SPREADSHEET_NAME = "Suivi paris"
SPREADSHEET_INDEX = 6               # index of 'Baseball Japan RAW', starting from 0


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def retrieve_month_results(year_to_get, month_to_get, league_to_get, from_day, to_day):

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

    logging.debug(url)
    wholepage = requests.get(url)

    allmatches_regex = re.compile('<a href="[a-zA-Z0-9\.\/]*">[A-Z]{1,2} [0-9*]{1,3} - [0-9*]{1,2} [A-Z]{1,2}')
    matchresult_regex = re.compile('([A-Z]{1,2} [0-9*]{1,3} - [0-9*]{1,2} [A-Z]{1,2})')

    allmatches = allmatches_regex.findall(wholepage.text)

    month_results = []

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
            month_results.append([match_day[6:9] + "/" + match_day[4:6] + "/" + match_day[0:4], league_to_get, match_result])
    
    return month_results


def retrieve_results(start_year, start_month, start_day, to_year, to_month, to_day, league_to_get):

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

        month_results = retrieve_month_results(str(current_year), str(current_month), league_to_get, local_from_day, local_to_day)
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

def upload_results(results):

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    #creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    
    credentials = {
        "type": "service_account",
        "project_id": os.getenv('SA_PROJECT_ID'),
        "private_key_id": os.getenv("SA_PRIVATE_KEY_ID"),
        "private_key": os.getenv("SA_PRIVATE_KEY"),
        "client_email": os.getenv("SA_CLIENT_EMAIL"),
        "client_id": os.getenv("SA_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv("SA_CLIENT_X509_CERT_URL")
    }
    creds = gspread.service_account_from_dict(credentials)
    client = gspread.authorize(creds)

    jpn_raw_sheet = client.open(SPREADSHEET_NAME).get_worksheet(SPREADSHEET_INDEX)

    for result in results:
        next_row = next_available_row(jpn_raw_sheet)
        jpn_raw_sheet.insert_row(['temp'], int(next_row))
        jpn_raw_sheet.update(
            'A' + next_row + ':U' + next_row,
            [
                [
                    result[0],
                    '=WEEKDAY(A' + next_row + ';2)',
                    result[1],
                    '=IF(G'+next_row+'<K'+next_row+';G'+next_row+';K'+next_row+')',
                    '=IF(G'+next_row+'>K'+next_row+';G'+next_row+';K'+next_row+')',
                    result[2],
                    '=SPLIT(F'+next_row+';" ")',
                    '',
                    '',
                    '',
                    '',
                    '=IF(H'+next_row+'="*";0;1)',
                    '=IF(L'+next_row+'=0;"*";IF(H'+next_row+'>J'+next_row+';G'+next_row+';K'+next_row+'))',
                    '=IF(L'+next_row+'=1;$H'+next_row+'+$J'+next_row+';"")',
                    '=IF(AND(L'+next_row+'=1;N'+next_row+'>3,5);1;0)',
                    '=IF(AND(L'+next_row+'=1;N'+next_row+'>4,5);1;0)',
                    '=IF(AND(L'+next_row+'=1;N'+next_row+'>5,5);1;0)',
                    '=IF(AND(L'+next_row+'=1;N'+next_row+'>6,5);1;0)',
                    '=IF(AND(L'+next_row+'=1;N'+next_row+'>7,5);1;0)',
                    '=IF(AND(L'+next_row+'=1;N'+next_row+'>8,5);1;0)',
                    '=IF(AND(L'+next_row+'=1;N'+next_row+'>9,5);1;0)'
                ]
            ],
            raw=False
        )

#
# Documentation Printing Method
#
def printDocumentation():

    print("args 'from:YYYYMMDD'. If not set, default value is today.")
    print("args 'to:YYYYMMDD'. If not set, default value is today.")
    print("args 'yesterday': set FROM and TO date limits at yesterday's date.")
    print("args 'upload', set to yes or no, to upload to spreadsheet.")

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

    upload = True

    for args in sys.argv:

        if args.startswith("from:"):
            start_year = args[5:9]
            start_month = args[9:11]
            start_day = args[11:13]

        elif args.startswith("to:"):
            to_year = args[3:7]
            to_month = args[7:9]
            to_day = args[9:11]

        elif args == "yesterday":
            yesterday = date.today() - timedelta(days=1)

            start_year = yesterday.strftime("%Y")
            start_month = yesterday.strftime("%m")
            start_day = yesterday.strftime("%d")

            to_year = yesterday.strftime("%Y")
            to_month = yesterday.strftime("%m")
            to_day = yesterday.strftime("%d")

        elif args.lower() == "upload:yes":
            upload = True

        elif args.lower() == "upload:no":
            upload = False

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

    results = retrieve_results(start_year, start_month, start_day, to_year, to_month, to_day, 'Regular Season')

    if(upload):
        upload_results(results)
import sys, logging
from main_local_helper import LocalExecHelper
from datetime import date, timedelta, datetime
from NPBCrawler import NPBCrawler
from SpreadSheetHelper import SpreadSheetHelper

#
# Documentation Printing Method
#
def printDocumentation():

    print("args 'from:YYYYMMDD'. If not set, default value is today.")
    print("args 'to:YYYYMMDD'. If not set, default value is today.")
    print("args 'yesterday': set FROM and TO date limits at yesterday's date.")
    print("args 'upload', set to yes or no, to upload to spreadsheet.")
    print("args 'local_exec' to load required environment variables")

#
# Main Function
#
if __name__ == '__main__':
    
    logging.getLogger().setLevel(logging.WARN)

    today = date.today()
    print("running datetime:", datetime.now())

    # defining default start date from which retrieving results
    start_year = today.strftime("%Y")
    start_month = today.strftime("%m")
    start_day = today.strftime("%d")

    # defining default end date to which retrieving results
    to_year = today.strftime("%Y")
    to_month = today.strftime("%m")
    to_day = today.strftime("%d")

    # securizing uploading: by default, we stay local
    upload = False

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

        elif args == "local_exec":
            LocalExecHelper()

    # verifying parameters are compatible
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

    # retrieving results from NPB website
    print("retrieving result from: " + start_year + "/" + start_month + "/" + start_day)
    crawler = NPBCrawler()
    results = crawler.retrieve_results(start_year, start_month, start_day, to_year, to_month, to_day, 'Regular Season')

    if(upload):
        helper = SpreadSheetHelper()
        helper.upload_results(results)
import sys, logging, os
from main_local_helper import LocalExecHelper
from datetime import date, timedelta, datetime
from NPBCrawler import NPBCrawler
from SpreadSheetHelper import SpreadSheetHelper

#
# Documentation Printing Method
#
def printDocumentation():

    print("args 'from:YYYYMMDD'. If not set, default value is today. Use 'from:complete_spreadsheet' to retrieve results using last date retrieved in remote spreadsheet.")
    print("args 'to:YYYYMMDD'. If not set, default value is today.")
    print("args 'yesterday': set FROM and TO date limits at yesterday's date.")
    print("args 'upload', set to yes or no, to upload to spreadsheet.")
    print("args 'local_exec' to load required environment variables. Must be first argument, to let others working.")

#
# Main Function
#
if __name__ == '__main__':
    
    logging.getLogger().setLevel(logging.INFO)

    today = date.today()
    logging.info("running datetime: " + str(datetime.now()))

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

        if args == "from:complete_spreadsheet":
            helper = SpreadSheetHelper()
            last_result_date = helper.get_last_result_date()
            last_result_date = datetime.strptime(last_result_date, '%d/%m/%Y')
            last_result_date = last_result_date + timedelta(days=1)

            start_year = last_result_date.strftime("%Y")
            start_month = last_result_date.strftime("%m")
            start_day = last_result_date.strftime("%d")

            to_year = last_result_date.strftime("%Y")
            to_month = last_result_date.strftime("%m")
            to_day = last_result_date.strftime("%d")
        
        elif args.startswith("from:"):
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
    crawler = NPBCrawler()
    results = crawler.retrieve_results(start_year, start_month, start_day, to_year, to_month, to_day, 'Regular Season')

    if(upload):
        helper = SpreadSheetHelper()
        helper.upload_results(results)
    
    os.environ["SCRIPT_RESULT"]='coucou'
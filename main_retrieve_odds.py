from baseball_japan.WinamaxCrawler import WinamaxCrawler
import logging
import os
import sys
from mongodb.BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper


#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    try:
        os.environ["MONGODB_NAME"]
    except KeyError:
        LocalExecHelper()

    # retrieving odds from Winamax
    crawler = WinamaxCrawler()
    matches = crawler.retrieve_odds()
        
    # inserting data in MongoDB
    mongodb = BetsMongoDB()
    for match in matches:
        mongodb.insertMatchOrAppendOdds(match)

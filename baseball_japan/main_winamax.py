from WinamaxCrawler import WinamaxCrawler
import logging
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from mongodb.BetsMongoDB import BetsMongoDB
from LocalExecHelper import LocalExecHelper


#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    crawler = WinamaxCrawler()
    matches = crawler.retrieve_odds()

    LocalExecHelper()
    mongodb = BetsMongoDB()
    for match in matches:
        mongodb.insertMatchOrAppendOdds(match)



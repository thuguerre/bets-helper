# Standard Library imports
import os
import sys
import logging

# Local imports
import localcontextloader
from baseball_japan.WinamaxCrawler import WinamaxCrawler
from mongodb.BetsMongoDB import BetsMongoDB


#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    # retrieving odds from Winamax
    crawler = WinamaxCrawler()
    matches = crawler.retrieve_odds()
        
    # inserting data in MongoDB
    mongodb = BetsMongoDB()
    for match in matches:
        mongodb.insertMatchOrAppendOdds(match)

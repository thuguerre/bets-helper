from WinamaxCrawler import WinamaxCrawler
import logging

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    crawler = WinamaxCrawler()
    crawler.test()


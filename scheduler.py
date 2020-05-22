
import datetime
import os
import random
import logging
from twisted.internet import reactor
from apscheduler.schedulers.twisted import TwistedScheduler

import time
import sys
import glob
import os
import shutil
from scrapy.crawler import CrawlerProcess
from scrapy.settings import default_settings
from util.util import *
from util.logger import set_params
from util.root import from_root
from util.report import notify
from util.healthcheck import check_rows
from crawlers.spiders.cl_listings_html import ApaSpider, DeltaApaSpider
from crawlers.spiders.cl_listings_roo import RooSpider, DeltaRooSpider
from crawlers.spiders.cl_listings_local import CLLSpider




def ArchiveProcess(ad_type):
    '''
    Define a CrawlerProcess
        : param ad_type: determines the path for 'FEED_URI'. Only accepts either 'apa' or 'roo'.
        :return: process -- a CrawlerProcess

    '''
    month = datetime.date.today().strftime("%Y-%m") 
    process = CrawlerProcess({
            'USER_AGENT': default_settings.USER_AGENT,
            'FEED_FORMAT': 'csv',
            'FEED_URI': "../results/parsed_raw/" + ad_type + "/listings-" + month + ".csv"
        })
    return process


   

def getFiles(ad_type):
    # Get directory in the form of yy-mm but for the previous month
    '''
    Find a list of HTML file path for the archive spiders to crawl. The function should return all HTML file path (of a specific ad type)
    that are scraped during the previous month and stored locally. 

    For example, if the current month is April 2020, and ad_type = 'apa', then the function will return all HTML paths in: '../results/raw_html/apa/2020-03'.

        :param ad_type: determines the path of the folder to look for HTML files. Only accepts either 'apa' or 'roo'.
        
        :return: all_filenames: a list of html file paths in the folder specified by 'ad_type' and current month
    '''  
    
        
    directory = last_month()
   
    extension = 'html'
    os.chdir('../results') 
    #path = "../results/raw_html/" + directory +'/*.{}'
    #if not os.path.exists("../results/raw_html/" + directory):
    path = "raw_html/" + ad_type + "/" + directory +'/*.{}'
    if not os.path.exists("raw_html/" + ad_type + "/" + directory):
        print('The directory: <' + str(directory) +'> does not exist in '+ "raw_html/" + ad_type )
        exit 

 
    all_filenames = ['file://' + os.getcwd() + '/' + i for i in glob.glob(path.format(extension))]
    return all_filenames



if __name__ == '__main__':
    print('Reminder: Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # initiate logger to store error message
    logger = logging.getLogger(__name__)
    #logger.setLevel(logging.DEBUG)
    set_params(logger, from_root("../log/scheduler.log"))

    scheduler = TwistedScheduler()

    process = CrawlerProcess()
    ## On the first day of each month, disable and reset scrapy deltafetch, retrieve all available ads on the domain
    scheduler.add_job(process.crawl, 'cron', args =[ApaSpider], day='1', hour=8, minute=rand_min())
    scheduler.add_job(process.crawl,'cron', args=[RooSpider], day='1', hour=8, minute=rand_min())

    ## On every day starting on the 2nd day of the month, enable scrapy deltafetch so that the scarper skips duplicates
    scheduler.add_job(process.crawl, 'cron', args =[DeltaApaSpider], day= '2/1', hour=13, minute=rand_min())
    scheduler.add_job(process.crawl,'cron', args=[DeltaRooSpider], day= '2/1',  hour=13, minute=rand_min())

    process1 = ArchiveProcess('apa')
    process2 = ArchiveProcess('roo')

    ## On every second day of the month, scrape archived HTML from the previous month into a .csv file
    scheduler.add_job(process1.crawl, 'cron', args=[CLLSpider], kwargs = {"start_urls" :getFiles('apa')}, day = '2', hour=17, minute=rand_min())
    scheduler.add_job(process2.crawl, 'cron', args=[CLLSpider], kwargs = {"start_urls" :getFiles('roo')}, day = '2', hour=17, minute=rand_min())
    scheduler.add_job(check_rows,'cron',args=["listings-" + last_month() + ".csv"], day = '22', hour=13, minute=40)

    scheduler.start()
    process.start()
    process1.start()
    process2.start()
   



    #Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        reactor.run()
  
    except (SystemExit):
        logger.warn("Scheduler: System Exit")
    #     notify("forcequit")
    #     reactor.stop()
    #     print("Finish executing script.")
    except (Exception):
        logger.warn("Scheduler: Exception")
       
        # logger.exception("Scheduler: Fatal Error")
        # notify("forcequit")
    except (KeyboardInterrupt):
        logger.warn("Scheduler: KeyboardInterrupt")
       
        # notify("forcequit")
        # reactor.stop()
        # print("Finish executing script.")
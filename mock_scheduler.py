
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
from util.util import getArg
from util.logger import set_params
from util.root import from_root
from crawlers.spiders.cl_listings_html import ApaSpider, DeltaApaSpider
from crawlers.spiders.cl_listings_roo import RooSpider, DeltaRooSpider
from crawlers.spiders.cl_listings_local import CLLSpider



def ArchiveProcess(ad_type):
    month = datetime.date.today().strftime("%Y-%m") 
    process = CrawlerProcess({
            'USER_AGENT': default_settings.USER_AGENT,
            'FEED_FORMAT': 'csv',
            'FEED_URI': "../results/parsed_raw/" + ad_type + "/listings-" + month + ".csv"
        })
    return process
        

def getFiles(ad_type):
    # Get directory in the form of yy-mm but for the previous month
    month = datetime.date.today().month 
    if month == 1:
        directory = str(datetime.date.today().year) + '-12' 
    elif month < 10:
        directory = str(datetime.date.today().year) + '-0' + str(month)
    else:
        directory = str(datetime.date.today().year) + '-' + str(month)
        

   
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

    logger = logging.getLogger(__name__)
    set_params(logger, from_root("log\\scheduler.log"))

    scheduler = TwistedScheduler()

    process = CrawlerProcess()
    scheduler.add_job(process.crawl, 'cron', args =[ApaSpider], day='1', hour=8, minute=30)
    scheduler.add_job(process.crawl,'cron', args=[RooSpider], day='1', hour=8, minute=0)
    scheduler.add_job(process.crawl, 'cron', args =[DeltaApaSpider], day= '2/1', hour=13, minute=20)
    scheduler.add_job(process.crawl,'cron', args=[DeltaRooSpider], day= '2/1',  hour=13, minute=25)

    process1 = ArchiveProcess('apa')
    process2 = ArchiveProcess('roo')
    scheduler.add_job(process1.crawl, 'cron', args=[CLLSpider], kwargs = {"start_urls" :getFiles('apa')}, day = '2', hour=17, minute=00)
    scheduler.add_job(process2.crawl, 'cron', args=[CLLSpider], kwargs = {"start_urls" :getFiles('roo')}, day = '2', hour=17, minute=15)
    
    scheduler.start()
    process.start()
    process1.start()
    process2.start()
   



    #Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        reactor.run()
  
    except (SystemExit):
        pass
    except (Exception):
        logger.exception("Scheduler: Fatal Error")
    except (KeyboardInterrupt):
        reactor.stop()
        print("Finish executing script.")
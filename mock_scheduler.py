
import datetime
import os
import random

from twisted.internet import reactor
from apscheduler.schedulers.twisted import TwistedScheduler

import time
import sys
import glob
import os
import shutil
from scrapy.crawler import CrawlerProcess
from scrapy.settings import default_settings
from util import getArg, movefile
#from rental_crawlers.spiders.cl_listings import CLSpider
from rental_crawlers.spiders.cl_listings_html import ApaSpider, DeltaApaSpider
from rental_crawlers.spiders.cl_listings_roo import ROOSpider, DeltaROOSpider
from rental_crawlers.spiders.cl_listings_local import CLLSpider


def web_apa():
    #time.sleep(random.randint(1,15)*60)
    month = datetime.date.today().strftime("%Y-%m")

    print(str(datetime.datetime.now()) + ": Activate web spider for apa postings")



    folder = "../results/raw_html/apa/" + month    
    if not os.path.exists(folder):
        os.makedirs(folder)




    if datetime.date.today().day <= 1:
        print(str(datetime.datetime.now())+ ": Disable deltafetch")
        process = CrawlerProcess()
        process.crawl(CLWebSpider)
        process.start(False)
        movefile(folder)



    else:
        print(str(datetime.datetime.now())+ ": Enable deltafetch")
        process = CrawlerProcess()
        process.crawl(DeltaCLWebSpider)
        process.start(False)
        movefile(folder)


def web_roo():
    #time.sleep(random.randint(1,15)*60)
    month = datetime.date.today().strftime("%Y-%m")

    print(str(datetime.datetime.now())+ ": Activate web spider for roo postings")
  
    folder2= "../results/raw_html/roo/" + month   
   
    if not os.path.exists(folder2):
        os.makedirs(folder2)
            #os.chdir(folder)  




    if datetime.date.today().day <= 1:
        print(str(datetime.datetime.now())+ ": Disable deltafetch")

        process = CrawlerProcess()
        process.crawl(CLROOSpider)
        process.start(False)
        movefile(folder2)




    else:
        print(str(datetime.datetime.now())+ ": Enable deltafetch")
        

        process = CrawlerProcess()
        process.crawl(DeltaCLROOSpider)
        process.start(False)
        movefile(folder2)




def archive_mode():
    
print(str(datetime.datetime.now())+ ": Activate archive spider")


    time.sleep(random.randint(1,15)*60)

    #Gets today's date and returns it in isoformat YYYY-MM-DD
    date = datetime.date.today().strftime("%Y-%m-%d") 

    #Find the folder from last month
    month = date.today().month 
    if month == 1:
        directory = str(date.today().year-1) + '-12' 
    elif month < 10:
        directory = str(date.today().year) + '-0' + str(month-1)
    else:
        directory = str(date.today().year) + '-' + str(month-1)
        
    

    for ad_type in ['apa','roo']:


    
        process = CrawlerProcess({
            'USER_AGENT': default_settings.USER_AGENT,
            'FEED_FORMAT': 'csv',
            'FEED_URI': "../results/parsed_raw/" + ad_type + "/listings-" + date + ".csv"
        })
        
        extension = 'html'
        os.chdir('../results') 
        #path = "../results/raw_html/" + directory +'/*.{}'
        #if not os.path.exists("../results/raw_html/" + directory):
        path = "raw_html/" + ad_type + "/" + directory +'/*.{}'
        if not os.path.exists("raw_html/" + ad_type + "/" + directory):
            print('The directory: <' + str(directory) +'> does not exist in '+ "raw_html/" + ad_type )
            exit 

        prefix  = os.getcwd()
        all_filenames = ['file://' + prefix + '/' + i for i in glob.glob(path.format(extension))]
    
        
        process.crawl(CLLSpider,start_urls = all_filenames)
        # process.crawl(KJSpider)
        # Need Splash running for VSpider: docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
        # process.crawl(VSpider)
        process.start()

        time.sleep(10*60)



if __name__ == '__main__':
    print('Reminder: Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    scheduler = TwistedScheduler()
    # scheduler.add_job(web_apa, 'cron',day_of_week='mon-fri', hour=15, minute=30)
    # scheduler.add_job(web_roo,'cron', day_of_week='mon-fri', hour=16, minute=00)
    # scheduler.add_job(archive_mode, 'cron',day_of_week='mon-fri', hour=16, minute=30)
    
    process = CrawlerProcess()
    scheduler.add_job(process.crawl, 'cron', args =[ApaSpider], day='1', hour=8, minute=30)
    scheduler.add_job(process.crawl,'cron', args=[ROOSpider], day='1', hour=8, minute=0)
    scheduler.add_job(process.crawl, 'cron', args =[DeltaApaSpider], day_of_week = 'mon - sun', hour=10, minute=30)
    scheduler.add_job(process.crawl,'cron', args=[DeltaROOSpider], day_of_week = 'mon - sun',  hour=16, minute=0)

    scheduler.add_job(archive_mode, 'cron', day ='25', hour=15, minute=45)
    
    scheduler.start()
    process.start(False)
   



    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    # try:
    #     reactor.run()
    # except (SystemExit):
    #     pass
    # except (KeyboardInterrupt):
    #     reactor.stop()
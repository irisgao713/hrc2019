import sched, time, threading, signal
from datetime import timedelta
from timeloop import Timeloop
import scrapy
import datetime
import random
import time
import sys
import glob
import os
import shutil
from scrapy.crawler import CrawlerProcess
from scrapy.settings import default_settings
from util import getArg, movefile
from rental_crawlers.spiders.cl_listings import CLSpider
from rental_crawlers.spiders.cl_listings_html import CLWebSpider, DeltaCLWebSpider
from rental_crawlers.spiders.cl_listings_roo import CLROOSpider, DeltaCLROOSpider
from rental_crawlers.spiders.cl_listings_local import CLLSpider




tl = Timeloop()


# Scrape HTMLs every 5 days
@tl.job(interval=timedelta(hours=1))
def web_mode():
    time.sleep(random.randint(1,15)*60)
    month = datetime.date.today().strftime("%Y-%m")

    print(datetime.date.today().strftime("%Y-%m-%d")+": Activate web spider")



    folder = "../results/raw_html/apa/" + month    
    folder2= "../results/raw_html/roo/" + month   
    if not os.path.exists(folder):
        os.makedirs(folder)
    elif not os.path.exists(folder2):
        os.makedirs(folder2)
            #os.chdir(folder)  




    if datetime.date.today().day <= 1:
        print("Disable deltafetch")
        process = CrawlerProcess()
        process.crawl(CLWebSpider)
        process.start()
        movefile(folder)

        process = CrawlerProcess()
        process.crawl(CLROOSpider)
        process.start()
        movefile(folder2)




    else:
        print("Enable deltafetch")
        process = CrawlerProcess()
        process.crawl(DeltaCLWebSpider)
        process.start()
        movefile(folder)

        process = CrawlerProcess()
        process.crawl(DeltaCLROOSpider)
        process.start()
        movefile(folder2)



# @tl.job(interval=timedelta(seconds=10))
# def tens_job():
#     print("10s job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(hours = 1))
def archive_mode():
    

    if datetime.date.today().day == 1:
        print(datetime.date.today().strftime("%Y-%m-%d")+": Activate archive spider")


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

            time.sleep(15*60)




# class Job(threading.Thread):
#     def __init__(self, interval, execute, *args, **kwargs):
#         threading.Thread.__init__(self)
#         self.daemon = False
#         self.stopped = threading.Event()
#         self.interval = interval
#         self.execute = execute
#         self.args = args
#         self.kwargs = kwargs
        
#     def stop(self):
#                 self.stopped.set()
#                 self.join()
#     def run(self):
#             while not self.stopped.wait(self.interval.total_seconds()):
#                 self.execute(*self.args, **self.kwargs)
            
if __name__ == "__main__":

    tl.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            tl.stop()
            break
    

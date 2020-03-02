import sched, time, threading, signal
from datetime import timedelta
from timeloop import Timeloop
#import scrapy
import datetime
import random
import time
import sys
import glob
import os
import shutil
#from scrapy.crawler import CrawlerProcess
#from scrapy.settings import default_settings
#from get_arg import getArg
# from rental_crawlers.spiders.cl_listings import CLSpider
# from rental_crawlers.spiders.cl_listings_html import CLWebSpider, DeltaCLWebSpider
# from rental_crawlers.spiders.cl_listings_roo import CLROOSpider, DeltaCLROOSpider
# from rental_crawlers.spiders.cl_listings_local import CLLSpider
# from movefile import movefile



tl = Timeloop()


# Scrape HTMLs every 5 days
@tl.job(interval=timedelta(days = 1))
def web_mode():
    #time.sleep(random.randint(1,15)*60)

    print(datetime.date.today().strftime("%Y-%m-%d") )

    if datetime.date.today().day <= 1:
        print('First time crawling, should disable deltafetch')




    else:
       print('Not first day, enable deltafetch')



# @tl.job(interval=timedelta(seconds=10))
# def tens_job():
#     print("10s job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(days = 1))
def archive_mode():
    print(datetime.date.today().strftime("%Y-%m-%d") )

    if datetime.date.today().day == 1:


        #time.sleep(random.randint(1,15)*60)

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
            
        
        print('First day of the month, produce csv file from ' + directory)

    else:
        print('Not first day of the month, no archiving')

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)
            
if __name__ == "__main__":

    tl.start(block=True)
    

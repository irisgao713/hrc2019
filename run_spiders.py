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
from try_arg import tryarg
#from rental_crawlers.spiders.kj_listings import KJSpider
from rental_crawlers.spiders.cl_listings import CLSpider
from rental_crawlers.spiders.cl_listings_html import CLWebSpider
#from rental_crawlers.spiders.cl_listings_archived import CLASpider
from rental_crawlers.spiders.cl_listings_local import CLLSpider
# from rental_crawlers.spiders.v_listings import VSpider
from movefile import movefile

time.sleep(random.randint(1,15)*60)

#Gets today's date and returns it in isoformat YYYY-MM-DD
month = datetime.date.today().strftime("%Y-%m-%d")

mode, directory = tryarg(sys.argv)


if mode == 'archive':
    # FEED_FORMAT is the output file type (accepts csv, json)
    # FEED_URI is the name of the output file (if no path specified, will put in same folder as where script is)
    process = CrawlerProcess({
        'USER_AGENT': default_settings.USER_AGENT,
        'FEED_FORMAT': 'csv',
        'FEED_URI': "../results/parsed_raw/listings-" + month + ".csv"
    })
    
    extension = 'html'
    os.chdir('../results') 
    #path = "../results/raw_html/" + directory +'/*.{}'
    #if not os.path.exists("../results/raw_html/" + directory):
    path = "raw_html/" + directory +'/*.{}'
    if not os.path.exists("raw_html/" + directory):
        print('The directory: ' + str(directory) +' does not exist!')
        exit 

    prefix  = os.getcwd()
    all_filenames = ['file://' + prefix + '/' + i for i in glob.glob(path.format(extension))]
   
     
    process.crawl(CLLSpider,start_urls = all_filenames)
    # process.crawl(KJSpider)
    # Need Splash running for VSpider: docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
    # process.crawl(VSpider)
    process.start()


elif mode == 'web':
    month = datetime.date.today().strftime("%Y-%m-%d")


    folder = "../results/raw_html/" + month       
    if not os.path.exists(folder):
        os.makedirs(folder)
        #os.chdir(folder)  

    process = CrawlerProcess()
    process.crawl(CLWebSpider)
    process.start()
    movefile(folder)

elif mode == 'normal':
    process = CrawlerProcess({
        'USER_AGENT': default_settings.USER_AGENT,
        'FEED_FORMAT': 'csv',
        'FEED_URI': "../results/raw/listings-" + month + ".csv"
    })
    process.crawl(CLSpider)
    process.start()

else:
    print ('Please use one of the following modes: web, archive, normal')
    exit
    
# def movefile(dstDir):
#     srcDir = ''
#     path = srcDir + '*.{}'
#     if os.path.isdir(dstDir) :
#         # Iterate over all the files in source directory
#         for filePath in glob.glob(path.format('html')):
#             # Move each file to destination Directory
#             shutil.move(filePath, dstDir)
#     else:
#         'Can not move htmls to designated folder'
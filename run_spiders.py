import scrapy
import datetime
import random
import time
import sys
import glob
import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings import default_settings
from util import getArg
from rental_crawlers.spiders.cl_listings import CLSpider
from rental_crawlers.spiders.cl_listings_html import ApaSpider, DeltaApaSpider
from rental_crawlers.spiders.cl_listings_roo import ROOSpider, DeltaROOSpider
from rental_crawlers.spiders.cl_listings_local import CLLSpider
from twisted.internet import reactor



#Gets today's date and returns it in isoformat YYYY-MM-DD
date = datetime.date.today().strftime("%Y-%m-%d") 
month = datetime.date.today().strftime("%Y-%m")

mode, directory = getArg(sys.argv)

if mode == 'archive_apa':
    ## apa
    process1 = CrawlerProcess({
            'USER_AGENT': default_settings.USER_AGENT,
            'FEED_FORMAT': 'csv',
            'FEED_URI': "../results/parsed_raw/apa/listings-" + directory + ".csv"
        })
        
    extension = 'html'
    os.chdir('../results') 
    #path = "../results/raw_html/" + directory +'/*.{}'
    #if not os.path.exists("../results/raw_html/" + directory):
    path = "raw_html/apa/" + directory +'/*.{}'
    if not os.path.exists("raw_html/apa/" + directory):
        print('The directory: <' + str(directory) +'> does not exist in '+ "raw_html/apa" )
        exit 

    prefix  = os.getcwd()
    all_filenames = ['file://' + prefix + '/' + i for i in glob.glob(path.format(extension))]

    
    process1.crawl(CLLSpider,start_urls = all_filenames)

elif mode =='archive_roo':

    #### roo
    process2 = CrawlerProcess({
            'USER_AGENT': default_settings.USER_AGENT,
            'FEED_FORMAT': 'csv',
            'FEED_URI': "../results/parsed_raw/roo/listings-" + directory + ".csv"
        })
    
    extension = 'html'
    os.chdir('../results') 
    #path = "../results/raw_html/" + directory +'/*.{}'
    #if not os.path.exists("../results/raw_html/" + directory):
    path = "raw_html/roo/" + directory +'/*.{}'
    if not os.path.exists("raw_html/roo/" + directory):
        print('The directory: <' + str(directory) +'> does not exist in '+ "raw_html/roo" )
        exit 

    prefix  = os.getcwd()
    all_filenames = ['file://' + prefix + '/' + i for i in glob.glob(path.format(extension))]

    
    process2.crawl(CLLSpider,start_urls = all_filenames)
    process2.start()



elif mode == 'apa':
    
    folder = "../results/raw_html/apa/" + month       
    if not os.path.exists(folder):
        os.makedirs(folder)
        #os.chdir(folder)  

    process = CrawlerProcess()
    process.crawl(DeltaApaSpider)
    process.start()
    
    
        


elif mode == 'normal':
    process = CrawlerProcess({
        'USER_AGENT': default_settings.USER_AGENT,
        'FEED_FORMAT': 'csv',
        'FEED_URI': "../results/raw/"+ month +"/listings-" + date + ".csv"
    })
    process.crawl(CLSpider)
    process.start()



elif mode == 'roo':
    # process = CrawlerProcess({
    #     'USER_AGENT': default_settings.USER_AGENT,
    #     'FEED_FORMAT': 'csv',
    #     'FEED_URI': "../results/raw/ROO_listings-" + date + ".csv"
    # })
    # process.crawl(CLROOSpider)
    # process.start()
    folder2 = "../results/raw_html/roo/"  + month       
    if not os.path.exists(folder2):
        os.makedirs(folder2)
        #os.chdir(folder)  

    process = CrawlerProcess()
    process.crawl(DeltaROOSpider)
    process.start()

else:
    print ('Please use one of the following modes: web, archive, normal')
    exit

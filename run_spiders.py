import scrapy
import datetime
import random
import time
import sys
import glob
import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings import default_settings
from util import getArg, movefile
#from rental_crawlers.spiders.cl_listings import CLSpider
from rental_crawlers.spiders.cl_listings_html import DeltaCLWebSpider,CLWebSpider
from rental_crawlers.spiders.cl_listings_roo import DeltaCLROOSpider, CLROOSpider
from rental_crawlers.spiders.cl_listings_local import CLLSpider
from twisted.internet import reactor

time.sleep(random.randint(1,15)*60)

#Gets today's date and returns it in isoformat YYYY-MM-DD
date = datetime.date.today().strftime("%Y-%m-%d") 
month = datetime.date.today().strftime("%Y-%m")

mode, directory = getArg(sys.argv)

if mode =='archive':

    ### apa
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

    # time.sleep(600)

    # #### roo
    # process2 = CrawlerProcess({
    #         'USER_AGENT': default_settings.USER_AGENT,
    #         'FEED_FORMAT': 'csv',
    #         'FEED_URI': "../results/parsed_raw/roo/listings-" + directory + ".csv"
    #     })
    
    # extension = 'html'
    # os.chdir('../results') 
    # #path = "../results/raw_html/" + directory +'/*.{}'
    # #if not os.path.exists("../results/raw_html/" + directory):
    # path = "raw_html/roo/" + directory +'/*.{}'
    # if not os.path.exists("raw_html/roo/" + directory):
    #     print('The directory: <' + str(directory) +'> does not exist in '+ "raw_html/roo" )
    #     exit 

    # prefix  = os.getcwd()
    # all_filenames = ['file://' + prefix + '/' + i for i in glob.glob(path.format(extension))]

    
    # process2.crawl(CLLSpider,start_urls = all_filenames)


elif mode == 'archiveOLD':
    # FEED_FORMAT is the output file type (accepts csv, json)
    # FEED_URI is the name of the output file (if no path specified, will put in same folder as where script is)
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
        # process.start()
        # process.addBoth(lambda _: reactor.stop())
        # reactor.run()


elif mode == 'web':
    
    folder = "../results/raw_html/apa/" + month       
    if not os.path.exists(folder):
        os.makedirs(folder)
        #os.chdir(folder)  

    process = CrawlerProcess()
    process.crawl(DeltaCLWebSpider)
    process.start()
    movefile(folder)

    folder2 = "../results/raw_html/roo/" + month       
    if not os.path.exists(folder2):
        os.makedirs(folder2)
        #os.chdir(folder)  

    process = CrawlerProcess()
    process.crawl(CLROOSpider)
    process.start()
    movefile(folder2)


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
    folder2 = "../results/raw_html/roo/" + month       
    if not os.path.exists(folder2):
        os.makedirs(folder2)
        #os.chdir(folder)  

    process = CrawlerProcess()
    process.crawl(DeltaCLROOSpider)
    process.start()
    movefile(folder2)

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
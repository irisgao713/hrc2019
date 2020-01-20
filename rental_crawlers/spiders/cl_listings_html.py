# -*- coding: utf-8 -*-
import scrapy
import sys
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from rental_crawlers.items import CLItem
import hashlib
import datetime

class CLWebSpider(CrawlSpider):

    name = 'cl_listings_html'
    allowed_domains = ['vancouver.craigslist.org']
    start_urls = [
        'https://vancouver.craigslist.org/search/apa'
        'https://vancouver.craigslist.org/d/rooms-shares/search/roo'
    ]
    #rooms for rent 'https://vancouver.craigslist.ca/rds/roo/' 
    #apartments 'https://vancouver.craigslist.ca/search/rds/apa'
    '''
    Rules for automatically following the links to the listing, and going to the next listing. 
    '''
    rules = (
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="result-title hdrlnk"]')), follow=True, callback='archive_listings'),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class, "button next")]')), follow=True, callback='archive_listings'),
        
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class, "next")]')), follow=True, callback='archive_listings'),
   
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="rows"]/li[1]/a')), follow=True, callback='parse_listings')
    )

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        #'DELTAFETCH_ENABLED': True,
        'DELTAFETCH_ENABLED': False,
        'SPIDER_MIDDLEWARES': {
            #'scrapy_deltafetch.DeltaFetch': 120,
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None
        },
        'ITEM_PIPELINES' : {
            'rental_crawlers.pipelines.CLPipeline': 300,
        }
    }

    '''
    Callback method for parsing the response text into a CLItem. 
    '''
    # def archive_listings(self, res):
    #     month = datetime.date.today().strftime("%Y-%m-%d")

    #     folder = "../results/raw_html/" + month 
    #     # if not os.path.exists(folder):
    #     #     os.mkdir(folder)

    #     path = folder + "/" + self.hash_url(res.url)
        
    #     with open(path, 'w+') as f:
    #         f.write(res.body)
    #         f.close


    def archive_listings(self, response):

        hashed_url = self.hash_url(response.url)   
        with open(hashed_url, 'w+') as f:
            f.write(response.body.decode("utf-8"))
            f.close()
        
        yield {
            'url': hashed_url
        }



    '''
    To generate file name from url instead of using url as file name
    '''
    def hash_url(self,url):
        return hashlib.sha224(str(url).encode('utf-8')).hexdigest()+'.html'

 

#terminal: scrapy crawl [name] -o [filename]

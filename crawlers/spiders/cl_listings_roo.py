# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlers.items import CLItem
import hashlib
import datetime


class DeltaRooSpider(CrawlSpider):

    name = 'cl_listings_roo_delta'
    allowed_domains = ['vancouver.craigslist.org']
    start_urls = [
        'https://vancouver.craigslist.org/d/rooms-shares/search/roo'
    ]

    '''
    Rules for automatically following the links to the listing, and going to the next listing. 
    '''
    rules = (
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="result-title hdrlnk"]')), follow=True, callback='parse_listings'),
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class, "button next")]')), follow=True, callback='parse_listings')
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class ="button next"]')), follow=True, callback='parse_listings'),
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class, "next")]')), follow=True, callback='archive_listings'),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="rows"]/li[@class="result-row"]/a')), follow=True, callback='parse_listings')
    
    )

    '''
    Settings for spider:
    1. Log level is set to information. When more details needed set LOG_LEVEL = DEBUG
    2. Enable scrapy deltafetch and add to middlewares
    3. Specify pipeline for all spiders, although for this spider it does nothing
    '''

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'DELTAFETCH_ENABLED': True,
        'CLOSESPIDER_ITEMCOUNT' : 900,
        'SPIDER_MIDDLEWARES': {
            'scrapy_deltafetch.DeltaFetch': 120,
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None
        },
        'ITEM_PIPELINES' : {
            'crawlers.pipelines.CLPipeline': 300,
        }
    }



    '''
    Callback method for parsing the response text into an HTML file. 
    '''

    def parse_listings(self, response):

        hashed_url = '../results/raw_html/roo/'+ datetime.date.today().strftime("%Y-%m")+'/'+ self.hash_url(response.url)   
        with open(hashed_url, 'w+') as f:
            f.write(response.body.decode("utf-8"))
            f.close()
        
        yield {
            'url': hashed_url
        }



    '''
    To generate hashed file name from url 
    '''
    def hash_url(self,url):
        return hashlib.sha224(str(url).encode('utf-8')).hexdigest()+'.html'




class RooSpider(CrawlSpider):

    name = 'cl_listings_roo'
    allowed_domains = ['vancouver.craigslist.org']
    start_urls = [
        'https://vancouver.craigslist.org/d/rooms-shares/search/roo'
    ]

    '''
    Rules for automatically following the links to the listing, and going to the next listing. 
    '''
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class ="button next"]')), follow=True, callback='parse_listings'),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="rows"]/li[@class="result-row"]/a')), follow=True, callback='parse_listings')
    
    )

    '''
    Settings for spider:
    1. Log level is set to information. When more details needed set LOG_LEVEL = DEBUG
    2. Disable scrapy deltafetch and reset status for the new month
    3. Specify pipeline for all spiders, although for this spider it does nothing
    '''
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'DELTAFETCH_ENABLED': False,
        'DELTAFETCH_RESET':True,
        'CLOSESPIDER_ITEMCOUNT' : 900,
        'SPIDER_MIDDLEWARES': {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None
        },
        'ITEM_PIPELINES' : {
            'crawlers.pipelines.CLPipeline': 300,
        }
    }



    '''
    Callback method for parsing the response text into an HTML file. 
    '''

    
    def parse_listings(self, response):

        hashed_url = '../results/raw_html/roo/'+ datetime.date.today().strftime("%Y-%m")+'/'+ self.hash_url(response.url)   
        with open(hashed_url, 'w+') as f:
            f.write(response.body.decode("utf-8"))
            f.close()
        
        yield {
            'url': hashed_url
        }



    '''
    To generate hashed file name from url 
    '''
    def hash_url(self,url):
        return hashlib.sha224(str(url).encode('utf-8')).hexdigest()+'.html'

#terminal: scrapy crawl [name] -o [filename]

# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from rental_crawlers.items import CLItem

class CLASpider(CrawlSpider):

    name = 'cl_listings_archived'
    

    # start_urls = [
    #     'https://vancouver.craigslist.org/search/apa'
    #     'https://vancouver.craigslist.org/d/rooms-shares/search/roo'
    # ]

    '''
    Rules for automatically following the links to the listing, and going to the next listing. 
    '''
    # rules = ( 
    #     Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="result-title hdrlnk"]')), follow=True, callback='parse_listings'),
    #     Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class, "button next")]')), follow=True, callback='parse_listings')
   
    #    # Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class, "button next")]')), follow=True, callback='parse_listings')
    # )

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        #'DELTAFETCH_ENABLED': True,
        'SPIDER_MIDDLEWARES': {
            #'scrapy_deltafetch.DeltaFetch': 120,
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None
        },
        'ITEM_PIPELINES' : {
            'rental_crawlers.pipelines.CLPipeline': 300,
        }
    }

    # custom_settings = {
    #     'LOG_LEVEL': 'DEBUG',
        
    #     'ITEM_PIPELINES' : {
    #         'rental_crawlers.pipelines.CLPipeline': 300,
    #     }
    # }

    '''
    Callback method for parsing the response text into a CLItem. 
    '''
    def parse_listings(self, response):
        item = CLItem()

        item['title'] = response.xpath('//span[@id="titletextonly"]/text()').extract_first()
        item['location'] = response.xpath('//small/text()').extract_first()
        item['sqft'] = response.xpath('//span[@class="housing"]/text()').extract_first()
        item['price'] = response.xpath('//span[@class="price"]/text()').extract_first()
        item['date'] = response.xpath('//time/@datetime').extract_first()
        item['lat'] = response.xpath('//div/@data-latitude').extract_first()
        item['long'] = response.xpath('//div/@data-longitude').extract_first()
        #item['description'] = response.xpath('//section[@id="postingbody"]/text()').extract_first()
        item['description'] = response.xpath('string(//section[@id="postingbody"])').extract()
        
        item['url'] = response.url
        item['source'] = "Craigslist"
        item['domain'] = response.xpath('//section/header[1]/nav/ul/li[2]/p/a/text()').extract_first()
        #NEW ITEMS

        item['location_accuracy'] = response.xpath('//div/@data-accuracy').extract_first()
        item['num_of_images']= len(response.xpath('//div[@class = "swipe-wrap"]/div').extract())

        map_address = response.xpath('//div[@class="mapaddress"]/text()')
        
        t1= response.xpath('//p[@class = "attrgroup"]/span[@class = "shared-line-bubble"]/b/text()').extract()
        t2 = response.xpath('//p[@class = "attrgroup"]/span/text()').extract()
        item['tags']= t1+t2

        if not len(map_address) < 1:
            item['map_address'] = map_address.extract_first()
        
        # if not len(tags) < 1 and not len(t2) < 1:
            # item['tags'] = tags.extract() 
        
        yield item

#terminal: scrapy crawl [name] -o [filename]

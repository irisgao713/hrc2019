# Rental Ads Crawling Tools

This repository contains scripts that scrape, store and preprocess housing listings from the _Craigslist_ website: https://vancouver.craigslist.org/.


## Overview

The crawling tools can execute the following tasks automatically:
1. Scrape listings from https://vancouver.craigslist.org/search/apa and https://vancouver.craigslist.org/search/roo and store them as HTML files locally.
2. Scrape local HTML files into a CSV file.
3. Monitor data quality on a monthly basis and send an e-mail notification in case of contamination.

All of the tasks above can be scheduled by the web crawler _'scheduler.py'_, which uses multiple single-purpose crawlers stored in the _crawlers_ folder. 


## Dependencies

- All code is written in Python3, using the Python Scrapy framework.
- Scrapy deltafetch depends on the bsddb3, Python bindings for Oracle Berkeley DB.
- Below is a list of frameworks that are required to run the scraper:
  - scrapy
  - twisted
- Below is a list of libraries that are required to be installed in a new environment:
  - pandas
  - numpy
  - hashlib
  - apscheduler
  - shutil
  - reportlab
  - django
  - email

  
  
## Description of files


<table>
  <thead>
    <tr>
       <th>Directory</th>
      <th>Filename</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>rental_crawler</td>
      <td>README.md</td>
      <td>Description of the project</td>
    </tr>
    <tr>
       <td></td>
      <td>scheduler.py</td>
      <td>Automate scraping from Craigslist. Involves multiple spiders.</td>
    </tr>
    <tr>
      <td></td>
      <td>run_spiders.py</td>
      <td>Run a crawl spider specified by input parameters</td>
    </tr>
    <tr>
      <td></td>
      <td>scrapy.cfg</td>
      <td>Scrapy's configuration settings</td>
    </tr>
    <tr>
      <td></td>
      <td>preprocessing.py</td>
      <td>Clean the CSV files and extract extra informations from several fields such as 'tags' and 'description'</td>
    </tr>
    <tr>
      <td>util</td>
      <td>util.py</td>
      <td>Helper functions</td>
    </tr>  
    <tr>
      <td></td>
      <td>logger.py</td>
      <td>Produce log file. Used in scheduler.py</td>
    </tr> 
    <tr>
      <td></td>
      <td>root.py</td>
      <td>Return root file path</td>
    </tr> 
    <tr>
      <td></td>
      <td>healthcheck.py</td>
      <td>Check if a CSV file has less than 100 rows or is empty, and send an alert if so</td>
    </tr> 
    <tr>
      <td></td>
      <td>report.py</td>
      <td>Send an email from scraperinfosender@yahoo.com as an alert that data is possibly contiminated</td>
    </tr> 
    <tr>
      <td></td>
      <td>attachments</td>
      <td>Email attachments that guides a user to restart the scraper</td>
    </tr> 
    <tr>
      <td>crawlers</td>
      <td>items.py</td>
      <td>Speficy the fields of a CL item</td>
    </tr> 
    <tr>
      <td></td>
      <td>middlewares.py</td>
      <td>Define models of the spider middlewares</td>
    </tr> 
    <tr>
      <td></td>
      <td>settings.py</td>
      <td>Scrapy settings for this project</td>
    </tr>
    <tr>
      <td>crawlers/spiders</td>
      <td>cl_basic.py</td>
      <td>Basic spider for baseline</td>
    </tr>
    <tr>
      <td></td>
      <td>cl_listings.py</td>
      <td>Scrape Craigslist sites and store listings in a CSV file</td>
    </tr> 
    <tr>
      <td></td>
      <td>cl_listings_apa.py</td>
      <td>Scrape Craigslist apartment rental postings and store listings as HTML files</td>
    </tr> 
    <tr>
      <td></td>
      <td>cl_listings_local.py</td>
      <td>Scrape local HTML files into a CSV file</td>
    </tr> 
    <tr>
      <td></td>
      <td>cl_listings_roo.py</td>
      <td>Scrape Craigslist room rental postings and store listings as HTML files</td>
    </tr> 
    <tr>
      <td></td>
      <td>kj_listings.py</td>
      <td>(Archive) Scrape kijiji postings and store listings as HTML files</td>
    </tr>
    <tr>
      <td></td>
      <td>v_listings.py</td>
      <td>(Archive) Scrape vrbo postings and store listings as HTML files</td>
    </tr> 
  </tbody>
</table>
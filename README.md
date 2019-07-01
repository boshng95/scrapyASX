# scrapyASX
Using Scrapy framework to parse ASX announcement data and to save it to the PostgreSQL

# Content of Project
The project contains 2 features:

i)  Parse all the annoucement from the link: https://www.asx.com.au/asx/statistics/todayAnns.do to PostgreSQL which contains ASX code, date time, price sensitivity with boolean, headline, page of annoucement report & URL link

ii) Parse all the open prices which contain in the annoucement link to PostgreSQL through pagination

# Getting Started (How to run this project)
To run this project, setting up of PostgreSQL & Python is required:

USERPATH\PycharmProjects\61FinTechChallenge\ASXAnnoucement\ASXAnnoucement\pipelines.py

PostgreSQL information need to be set up in pipelines.py
```python
self.connection = psycopg2.connect(
            host="localhost",
            port="5000",
            user="postgres",
            password="",
            dbname="")
```

# Libraries Used
```python
import scrapy
from scrapy.crawler import CrawlerProcess
import datetime
import pytz
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
from selenium import webdriver
import psycopg2
```

# Documentation of ScrapyASX

### testing.py
USERPATH\PycharmProjects\61FinTechChallenge\ASXAnnoucement\ASXAnnoucement\spiders\testing.py

This file is to scrap the data from annoucement page & scrap from pagination for prices.

### testing.py
USERPATH\PycharmProjects\61FinTechChallenge\ASXAnnoucement\ASXAnnoucement\pipelines.py

This file is to perform PostgreSQL query to parse the scraped data into database using psycopg2.




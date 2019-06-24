import scrapy
from scrapy.crawler import CrawlerProcess
import datetime
import pytz
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
from selenium import webdriver

'''
Parse the announcement on https://www.asx.com.au/asx/statistics/todayAnns.do
'''
class MySpider1(scrapy.Spider):

    name = 'asx'
    start_urls = ['https://www.asx.com.au/asx/statistics/prevBusDayAnns.do']
    annoucement = dict()

    def parse(self, response):

        companyCode = response.xpath('//tr//td[1]/text()').extract()

        date = response.xpath('//tr//td[2]/text()').extract()
        date = [x.strip() for x in date]  # strip all the blanks
        date = [x for x in date if x]  # remove all the blank elements

        timezone = pytz.timezone("Australia/Sydney")
        time = response.xpath('//tr//td[2]//span//text()').extract()
        dateTime = [m+" "+str(n) for m, n in zip(date, time)]
        dateTime = [datetime.datetime.strptime(x, '%d/%m/%Y %I:%M %p').strftime('%m/%d/%Y %H:%M') for x in dateTime]
        dateTime = [x+" "+timezone.zone for x in dateTime]

        priceSensitive = response.xpath('//tr//td[3]').extract()
        priceSensitive = [True if "img" in x else False for x in priceSensitive]

        headline = response.xpath('//tr//td[4]//a[1]/text()').extract()
        headline = [x.strip() for x in headline]  # strip all the blanks
        headline = [x for x in headline if x]  # remove all the blank elements

        pageCount = response.xpath('//tr//td[4]//a[1]//span[@class="page"]/text()').extract()
        pageCount = [x
                         .replace('\t', '')
                         .replace('\n', '')
                         .replace('\r', '')
                         .replace(' ', '')
                         .replace('page', '')
                         .replace('s', '') for x in pageCount] # strip all the blanks & "page/S" string

        urlLink = response.xpath('//tr//td[4]//a[1]/@href').extract()
        urlLink = ["https://www.asx.com.au" + x for x in urlLink if x]


        MySpider1.annoucement["asx_code"] = companyCode;
        MySpider1.annoucement["timestamp"] = dateTime;
        MySpider1.annoucement["price_sense"] = priceSensitive;
        MySpider1.annoucement["headline"] = headline;
        MySpider1.annoucement["page_count"] = pageCount;
        MySpider1.annoucement["url_link"] = urlLink;

        # for x in range(0, len(companyCode)):
        # print(companyCode[x]+" "+dateTime[x]+" "+str(priceSensitive[x])+" "+headline[x]+" "+pageCount[x]+" "+urlLink[x])

        yield MySpider1.annoucement


'''
Parse the prices according to each page using Beautiful Soup
'''
class MySpider2(scrapy.Spider):

    name = 'asx1'
    start_urls = ['https://www.asx.com.au/asx/statistics/todayAnns.do']
    prices = dict()

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):

        companyCode = response.xpath('//tr//td[1]/text()').extract()

        for x in range(0, len(companyCode)):
            extract_price = "https://www.asx.com.au/asx/share-price-research/company/"+companyCode[x]+"/statistics/shares"
            MySpider2.parse_price(self, extract_price, companyCode[x])

        yield MySpider2.prices

    def parse_price(self, url, code):

        self.driver.get(url)
        body = self.driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(body, 'lxml')
        tables = soup.find_all('table')
        rows = tables[0].find_all('tr')
        data = rows[2].find_all('td')[1].find_all('span')[0].text
        MySpider2.prices.update({code: data})


process = CrawlerProcess(get_project_settings())
process.crawl(MySpider1)
process.crawl(MySpider2)
process.start(stop_after_crawl=False)


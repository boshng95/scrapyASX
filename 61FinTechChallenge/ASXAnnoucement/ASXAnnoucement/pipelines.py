# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class AsxannoucementPipeline(object):

    def open_spider(self, spider):

        '''self.connection = psycopg2.connect(
            host="localhost",
            port="5000",
            user="postgres",
            password="",
            dbname="")'''

        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if spider.__class__.__name__ == "MySpider1":
            try:
                self.cur.execute("DELETE FROM ASX")
            except:
                self.connection.rollback()
                self.cur.execute("""CREATE TABLE ASX(annoucement_id SERIAL PRIMARY KEY,
                                asx_code character varying COLLATE pg_catalog."default",
                                date_time timestamp with time zone,
                                price_sens boolean,
                                headline character varying COLLATE pg_catalog."default",
                                page_count integer,
                                url_link character varying COLLATE pg_catalog."default",
                                close_price money);"""
                                 )

            self.cur.execute("ALTER SEQUENCE asx_annoucement_id_seq RESTART WITH 1")
            for x in range(0, len(item['asx_code'])):
                self.cur.execute("INSERT INTO ASX(asx_code,date_time, price_sens, headline, page_count, url_link) " +
                                "VALUES(%s, %s, %s, %s, %s, %s)"
                                 , (item['asx_code'][x],
                                    item['timestamp'][x],
                                    item['price_sense'][x],
                                    item['headline'][x],
                                    item['page_count'][x],
                                    item['url_link'][x]))
            print("Annoucment update")
            self.connection.commit()

        else:
            self.cur.execute("SELECT DISTINCT asx_code FROM ASX;")

            for code, price in item.items():
                self.cur.execute("UPDATE ASX SET close_price= (%s) WHERE asx_code= (%s)", (price, code))
                self.connection.commit()

        self.connection.close()
        return item

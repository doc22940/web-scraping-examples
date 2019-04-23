# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class AmazonBookPipeline(object):

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'test_user'
        password = 'test123'
        database = 'amazon_books_db'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if item["old_price"] is None:
            if item["new_price"] is None:
                self.cur.execute("insert into amazon_books.books(title, author, image_link) values(%s,%s,%s)",(
                    item['title'], item['author'], item['image_link']
                ))
            else:
                self.cur.execute("insert into amazon_books.books(title, author, new_price, image_link) values(%s,%s,%s,%s)",(
                    item['title'], item['author'], item['new_price'], item['image_link']
                ))
        else:
            self.cur.execute("insert into amazon_books.books(title, author, new_price, old_price, image_link) values(%s,%s,%s,%s,%s)",(
                item['title'], item['author'], item['new_price'], item["old_price"], item['image_link']
            ))
        
        self.connection.commit()
        return item

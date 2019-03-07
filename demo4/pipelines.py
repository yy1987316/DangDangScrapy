# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BookPipeline(object):
    def open_spider(self, spider):
        print('opened')
        self.count = 0

        try:
            self.con = pymysql.connect(host='127.0.0.1', port=3306, user='test', passwd='123456', charset='utf8')
            self.cursor = self.con.cursor(pymysql.cursors.DictCursor)
            try:
                self.cursor.execute('create database mydb')
            except:
                pass

            self.con.select_db('mydb')

            try:
                self.cursor.execute('drop table books')
            except:
                pass

            try:
                sql = '''
                create table books
(
	title varchar(512) primary key,
    author varchar(256),
    publisher varchar(256),
    date varchar(32),
    price varchar(16),
    detail text
)'''

                self.cursor.execute(sql)
            except:
                self.cursor.execute('delete from books')

            self.opened = True

        except Exception as err:
            print('BookPipeline.open_spider err:', err)
            self.opened = False


    def close_spider(self, spider):
        if self.opened:
            self.con.commit()
            self.con.close()
            self.opened = False
        print('closed')
        print('总共爬去', self.count, '本书籍')

    def process_item(self, item, spider):
        try:
            print(item['title'])
            print(item['author'])
            print(item['publisher'])
            print(item['date'])
            print(item['price'])
            print(item['detail'])
            print()
            if self.opened:
                self.cursor.execute('insert into books values(%s,%s,%s,%s,%s,%s)', (item['title'], item['author'], item['publisher'], item['date'], item['price'], item['detail']))
            self.count += 1
        except Exception as err:
            print('BookPipeline.process_item err:', err)
        return item

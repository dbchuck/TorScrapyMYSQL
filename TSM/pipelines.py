# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import SQL credetials
from scrapy.utils.project import get_project_settings
import mysql.connector
import re
import sys

# Stores items into SQL server database

class TsmPipeline(object):
    INDEX = 0

    # Connect to the MySQL server
    settings = get_project_settings()
    CONN = mysql.connector.connect(host=settings['SQL_HOST'],
                                   user=settings['SQL_USER'],
                                   passwd=settings['SQL_PASSWORD'],
                                   db=settings['SQL_DB'])
    cursor = CONN.cursor(buffered=True)

    def process_item(self, item):
        sql = "INSERT INTO %s (redirectURL, url, urlsFound, domain, title, h1, h2, timeFound) VALUES " % self.settings['MAIN_TABLE_NAME']
        sql += "(%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (item['redirectURL'], item['url'], item['urlsFound'], item['domain'], item['title'], item['h1'], item['h2'], item['timeFound'])
        self.cursor.execute(sql, values)
        self.CONN.commit()
        return item

    def check_duplicates(self, table, column, value):
        sql = "SELECT COUNT(%s) FROM %s WHERE %s='%s'" % (column, table, column, value)
        self.cursor.execute(sql)
        if self.cursor.fetchone()[0] >= 1:
            return False
        else:
            # No duplicates - good to insert
            return True

    def get_url(self):
        try:
            sql = "SELECT * FROM `%s` ORDER BY `%s`.`id` ASC LIMIT 1" % (self.settings['QUEUE_TABLE_NAME'], self.settings['QUEUE_TABLE_NAME'])
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            url = result[1]
            sql = "INSERT INTO %s (id, url) VALUES (NULL, '%s')" % (self.settings['IN_PROGRESS_TABLE_NAME'], result[1])
            self.cursor.execute(sql)
            self.CONN.commit()
            sql = "SELECT * FROM %s WHERE %s.url = '%s'" % (self.settings['IN_PROGRESS_TABLE_NAME'], self.settings['IN_PROGRESS_TABLE_NAME'], result[1])
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            global INDEX
            INDEX = result[0]
            sql = "DELETE FROM %s WHERE %s.id = '%s'" % (self.settings['QUEUE_TABLE_NAME'], self.settings['QUEUE_TABLE_NAME'], result[0])
            self.cursor.execute(sql)
            self.CONN.commit()
            return url
        except:
            print("ERROR: Database does not have any urls in the queue table '%s' in database '%s'" % (self.settings['QUEUE_TABLE_NAME'], self.settings['SQL_DB']))
            sys.exit(1)

    def add_url(self, url):
        sql = "INSERT INTO %s (id, url) VALUES " % (self.settings['QUEUE_TABLE_NAME'])
        sql += "(%s, %s)"
        parm = ("NULL", url)
        # Onion links only
        if re.match(r'(?:https?://)?(?:www)?(\S*?\.onion)\b', url, re.M | re.IGNORECASE):
            if self.check_duplicates(self.settings['QUEUE_TABLE_NAME'], "url", url) and self.check_duplicates(self.settings['IN_PROGRESS_TABLE_NAME'], "url", url) and self.check_duplicates(self.settings['FINISHED_TABLE_NAME'], "url", url):
                # its like this for sanitation purposes
                self.cursor.execute(sql, parm)
                self.CONN.commit()
        return None

    def url_finished(self):
        sql = "SELECT * FROM %s WHERE id = %s" % (self.settings['IN_PROGRESS_TABLE_NAME'], INDEX)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        sql = "INSERT INTO %s (id, url) VALUES (NULL, '%s')" % (self.settings['FINISHED_TABLE_NAME'], result[1])
        self.cursor.execute(sql)
        self.CONN.commit()
        sql = "DELETE FROM %s WHERE %s.id = %s" % (self.settings['IN_PROGRESS_TABLE_NAME'], self.settings['IN_PROGRESS_TABLE_NAME'], result[0])
        self.cursor.execute(sql)
        self.CONN.commit()
        return None

    def close_spider(self, spider):
        self.url_finished()
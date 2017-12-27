import mysql.connector
import sys
import re

# SQL DATABASE SETTING
SQL_DB = 'TorScrapyMYSQL'
SQL_HOST = 'localhost'
SQL_USER = 'TorScrapyMYSQL'
SQL_PASSWD = 'torScr4pingwith$crapy'
URL = ''
INDEX = 0

class SQLStorePipeline(object):

    # Connect to the MySQL server
    CONN = mysql.connector.connect(host=SQL_HOST,
                           user=SQL_USER,
                           passwd=SQL_PASSWD,
                           db=SQL_DB)
    cursor = CONN.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO main (redirectURL, url, urlsFound, domain, title, h1, h2, html_page, words, dateFound) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = ((item['redirectURL'], item['url'], item['urlsFound'], item['domain'], item['title'], item['h1'], item['h2'], item['html_page'], item['words'], item['dateFound']))
        # TODO: impliment no duplicate for 1 hour
        #if self.check_duplicates("TorScrapyMYSQL", "main", "url", item['url']):
        self.cursor.execute(sql, values)
        self.CONN.commit()
        return item

    def close_spider(self, spider):
        self.url_finished()

    def check_duplicates(self, table, column, value):
        sql = "SELECT COUNT(%s) FROM %s WHERE %s='%s'" % (column, table, column, value)
        self.cursor.execute(sql)
        if self.cursor.fetchone()[0] >= 1:
            return False
        else:
            # No duplicates - good to insert
            return True

    def get_url(self):
        sql = "SELECT * FROM `url_queue` ORDER BY `url_queue`.`id` ASC LIMIT 1"
        self.cursor.execute(sql)
        global URL
        URL = self.cursor.fetchone()[1]
        return URL

    def add_url(self, url):
        sql = "INSERT INTO url_queue (id, url) VALUES (NULL, '%s')" % (url)
        # Onion links only
        if re.match(r'(?:https?://)?(?:www)?(\S*?\.onion)\b', url, re.M | re.IGNORECASE):
            if self.check_duplicates("url_queue", "url", url) and self.check_duplicates("url_in_progress", "url", url) and self.check_duplicates("url_finished", "url", url):
                self.cursor.execute(sql)
                self.CONN.commit()
        return None

    def url_in_progress(self):
        sql = "SELECT * FROM `url_queue` ORDER BY `url_queue`.`id` ASC LIMIT 1"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        sql = "INSERT INTO url_in_progress (id, url) VALUES (NULL, '%s')" % result[1]
        self.cursor.execute(sql)
        self.CONN.commit()
        sql = "SELECT * FROM url_in_progress WHERE url_in_progress.url = '%s'" % result[1]
        self.cursor.execute(sql)
        global INDEX
        INDEX = self.cursor.fetchone()[0]
        sql = "DELETE FROM url_queue WHERE url_queue.id = '%s'" % result[0]
        self.cursor.execute(sql)
        self.CONN.commit()
        return None

    def url_finished(self):
        sql = "SELECT * FROM url_in_progress WHERE url_in_progress.id = %s" % INDEX
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        sql = "INSERT INTO url_finished (id, url) VALUES (NULL, '%s')" % result[1]
        self.cursor.execute(sql)
        self.CONN.commit()
        sql = "DELETE FROM url_in_progress WHERE url_in_progress.id = %s" % result[0]
        self.cursor.execute(sql)
        self.CONN.commit()
        return None

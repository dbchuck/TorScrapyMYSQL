from urllib.parse import urlparse, urlsplit
from posixpath import basename
import html2text
import re
import logging
import os
import os.path
import time
import timeit
from TorScrapyMYSQL.urlmarker import *
import scrapy
from scrapy.spiders import CrawlSpider
from TorScrapyMYSQL.items import CrawledWebsiteItem
from TorScrapyMYSQL.pipelines import *
from TorScrapyMYSQL.settings import *

class TorScrapyMYSQL(CrawlSpider):

    # Start the spider when in the same folder as this file by: scrapy crawl TorScrapyMYSQL
    name = "TorScrapyMYSQL"
    
    # Start SQL database connection
    sqlDB = SQLStorePipeline()

    # Add urls
    # Example domain: google.com
    start_url = sqlDB.get_url()
    allowed_domains = [urlparse(start_url).hostname]
    # Example url: http://.com
    start_urls = ["http://" + urlparse(start_url).hostname + "/"]
    sqlDB.url_in_progress()

    def parse(self, response):
        
        #print (response.meta['depth'])
        
        # Scrape information
        item = CrawledWebsiteItem()
        item['url'] = response.url
        item['domain'] = urlsplit(response.url).hostname
        title_list = response.css('title::text').extract()
        item['title'] = " ".join(title_list)
        h1_list = response.css('h1::text').extract()
        item['h1'] = " ".join(h1_list)
        h2_list = response.css('h2::text').extract()
        item['h2'] = " ".join(h2_list)
        encoding = self.detect_encoding(response)
        html = response.body.decode(encoding, "ignore")
        words = self.extract_words(self.html2string(html))
        item['words'] = " ".join(words)
        item['html_page'] = response.body
        urlsOnWebpage = []
        links = response.css('a::attr(href)').extract()
        text_links = re.findall(WEB_URL_REGEX, html2text.HTML2Text().handle(response.body.decode(encoding, "ignore")), re.M | re.IGNORECASE)
        urlsOnWebpage += text_links
        for link in links:
            url = response.urljoin(link)
            urlsOnWebpage.append(url)
            
            # Add offsite domains to url_queue
            url = "http://%s/" % (urlsplit(url).hostname)
            self.sqlDB.add_url(url)
        item['urlsFound'] = " ".join(urlsOnWebpage)
        try:
            item['redirectURL'] = ", ".join(response.meta['redirect_urls'])
        except:
            item['redirectURL'] = ""
        item['dateFound'] = time.strftime("%c")

        # Store scraped data into SQL database
        self.sqlDB.process_item(item, TorScrapyMYSQL)

        # Use previous links for crawling
        for link in urlsOnWebpage:
            link = response.urljoin(link)
            link_extension = (os.path.splitext(urlparse(link).path)[1])
            # Only follow pages that have this ending
            allowed_extensions = ['', '.html', '.php']
            
            if link_extension in allowed_extensions:
                # Only onion links
                if re.match(r'(?:https?://)?(?:www)?(\S*?\.onion)\b', link, re.M | re.IGNORECASE):
                    yield response.follow(link, callback=self.parse)

    def detect_encoding(self, response):
        return response.headers.encoding or "utf-8"

    def html2string(self, decoded_html):
        # HTML 2 string converter. Returns a string.
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        string = converter.handle(decoded_html)
        return string

    def extract_words(self, html_string):
        # Create a word list.
        string_list = re.split(r' |\n|#|\*', html_string)
        words = []
        for word in string_list:
            # Word must be longer than 0 letter
            # And shorter than 45
            # The longest word in a major English dictionary is
            # Pneumonoultramicroscopicsilicovolcanoconiosis (45 letters)
            if len(word) > 0 and len(word) <= 45:
                words.append(word)
        return words

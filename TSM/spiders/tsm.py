# -*- coding: utf-8 -*-
import time
import re
import scrapy
import os
import os.path
from urllib.parse import urlparse, urlsplit
from TSM.items import TsmItem
from TSM.pipelines import TsmPipeline
from scrapy.spiders import CrawlSpider


class TsmSpider(CrawlSpider):
    name = 'tsm'
    # Example:
    #
    # allowed_domains = ['mijpsrtgf54l7um6.onion']
    # start_urls = ['http://mijpsrtgf54l7um6.onion']
    #
    # With those settings, Scrapy will only parse the domain starting at the root of the website

    # Create connection to SQL database
    sqlDB = TsmPipeline()

    start_url = sqlDB.get_url()
    # Pipeline class takes the url out of queue
    allowed_domains = [urlparse(start_url).hostname]
    start_urls = ["http://" + urlparse(start_url).hostname + "/"]

    def parse(self, response):
        # The HTML body
        # print(response.body.decode(self.detect_encoding(response), "ignore"))

        # print (response.meta['depth'])

        # Scrape information
        item = TsmItem()
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
        urlsOnWebpage = []
        links = response.css('a::attr(href)').extract()

        for link in links:
            url = response.urljoin(link)
            urlsOnWebpage.append(url)

            # Attempt to add more offsite domains to queue
            url = "http://%s/" % urlsplit(url).hostname
            self.sqlDB.add_url(url)
        item['urlsFound'] = ",".join(urlsOnWebpage)
        try:
            item['redirectURL'] = ", ".join(response.meta['redirect_urls'])
        except:
            item['redirectURL'] = ""
        item['timeFound'] = time.strftime("%c")

        self.sqlDB.process_item(item)

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

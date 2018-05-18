# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TsmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """A web site"""
    domain = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    h1 = scrapy.Field()
    h2 = scrapy.Field()
    urlsFound = scrapy.Field()
    redirectURL = scrapy.Field()
    timeFound = scrapy.Field()

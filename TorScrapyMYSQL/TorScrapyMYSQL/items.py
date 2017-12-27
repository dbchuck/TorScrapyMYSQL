from scrapy.item import *

class CrawledWebsiteItem(Item):
    """A web site"""
    domain = Field()
    url = Field()
    title = Field()
    h1 = Field()
    h2 = Field()
    html_page = Field()
    words = Field()
    urlsFound = Field()
    redirectURL = Field()
    dateFound = Field()

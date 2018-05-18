# -*- coding: utf-8 -*-

# Scrapy settings for TSM project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'TSM'

SPIDER_MODULES = ['TSM.spiders']
NEWSPIDER_MODULE = 'TSM.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'TSM Bot v1.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 250

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Number of times to retry grabbing a webpage
RETRY_TIMES = 0

# Depth limit for webscraping from the original webpage (0 is unlimited)
DEPTH_LIMIT = 0

# The level of information to printed by the program to the screen
# Either DEBUG or INFO
LOG_LEVEL = 'INFO'

# The maximum time to wait for a DNS response in seconds
DNS_TIMEOUT = 5

# The maximum time to wait for a webserver to respond to request
DOWNLOAD_TIMEOUT = 15

# Scrapy uses this proxy for gathering the webpages
HTTP_PROXY = 'http://localhost:8118'

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
# Waits for an hour before grabbing page from the web again
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Login credtials for SQL database
SQL_HOST = 'localhost'
SQL_DB = 'tsm'
SQL_USER = 'tsm'
SQL_PASSWORD = 'tsm'

MAIN_TABLE_NAME = 'main'
QUEUE_TABLE_NAME = 'queue'
IN_PROGRESS_TABLE_NAME = 'in_progress'
FINISHED_TABLE_NAME = 'finished'

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'TSM.proxy.SimpleProxyMiddleware': 410
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'TSM.middlewares.TsmSpiderMiddleware': 543,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'TSM.pipelines.TsmPipeline': 300,
}
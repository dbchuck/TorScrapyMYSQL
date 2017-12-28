# -*- coding: utf-8 -*-

BOT_NAME = 'TorScrapyMYSQL'

SPIDER_MODULES = ['TorScrapyMYSQL.spiders']
NEWSPIDER_MODULE = 'TorScrapyMYSQL.spiders'

DEPTH_LIMIT = 0
LOG_LEVEL = 'DEBUG'
USER_AGENT = ''
CONCURRENT_REQUESTS = 100
DNS_TIMEOUT = 5
DOWNLOAD_TIMEOUT = 10

# use telnet console
TELNETCONSOLE_ENABLED = False
RETRY_TIMES = 2
# HTTP response codes to retry
RETRY_HTTP_CODES = [500, 502, 503, 504]
COOKIES_ENABLED = False

# TOR SETTINGS
HTTP_PROXY = 'http://127.0.0.1:8118'
AUTH_PASSWORD = 'secretPassword'
CONTROL_PORT = 9051
# number of HTTTP request before the IP change
# delete or set to None if you don't want to use it
MAX_REQ_PER_IP = 1000

# downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'TorScrapyMYSQL.proxy.TorProxyMiddleware': 410
}

ITEM_PIPELINES = {
    'TorScrapyMYSQL.pipelines.SQLStorePipeline': 100,
}

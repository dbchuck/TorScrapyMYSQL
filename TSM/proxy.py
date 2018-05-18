import logging
from scrapy.utils.project import get_project_settings

class SimpleProxyMiddleware(object):

    def __init__(self):
        self.import_settings()

    def import_settings(self):
        settings = get_project_settings()
        self.http_proxy = settings['HTTP_PROXY']

    def process_request(self, request, spider):
        request.meta['proxy'] = self.http_proxy
        logging.info('Using proxy: %s', request.meta['proxy'])
        return None
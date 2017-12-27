import random
import logging
import urllib
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings

class TorProxyMiddleware(object):

    def __init__(self):
        self.import_settings()
        self.req_counter = 0

    def change_ip_address(self):
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(self.password)
            controller.signal(Signal.NEWNYM)
            controller.close()

    def import_settings(self):
        settings = get_project_settings()
        self.password = settings['AUTH_PASSWORD']
        self.http_proxy = settings['HTTP_PROXY']
        self.control_port = settings['CONTROL_PORT']
        self.max_req_per_ip = settings['MAX_REQ_PER_IP']

    def process_request(self, request, spider):
        self.req_counter += 1
        if self.max_req_per_ip is not None and self.req_counter > self.max_req_per_ip:
            self.req_counter = 0
            self.change_ip_address()

        request.meta['proxy'] = self.http_proxy
        logging.info('Using proxy: %s', request.meta['proxy'])
        return None

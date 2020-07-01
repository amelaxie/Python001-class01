# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
from collections import defaultdict
from urllib.parse import urlparse
import random
import base64

class MytestSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    # def __init__(self, auth_encoding='utf-8', proxy_list = None):
    #     print ("in-------------------------------1")
    #     try:
    #         self.proxies = defaultdict(list)
    #         for proxy in proxy_list:
    #             parse = urlparse(proxy)
    #             self.proxies[parse.scheme].append(proxy)
    #     except Exception as e:
    #         print(e)

    def process_request(self,request,spider):
        if request.url.startswith("http://"):
            request.meta['proxy']="http://"+'122.51.139.61:18231'          # http代理
        elif request.url.startswith("https://"):
            request.meta['proxy']="https://"+'122.51.139.61:18231'         # https代理

    # @classmethod
    # def from_crawler(cls, crawler):
    #     try:
    #         if not crawler.settings.get('HTTP_PROXY_LIST'):
    #             raise NotConfigured

    #         http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
    #         auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
    #     except Exception as e:
    #         print(e)
    #     return cls(auth_encoding, http_proxy_list)

    # def _set_proxy(self, request, scheme):
    #     try:
    #         print("in-------------------------------1")
    #         proxy = random.choice(self.proxies[scheme])
    #         #request.meta['proxy'] = proxy
    #         request.meta['proxy'] = 'https://122.51.139.61:18231'
    #     except Exception as e:
    #         print(e)

        #proxy_user_pass = "newbie:pE5-Xtv#fS5McU6I"
        # setup basic authentication for the proxy
        #encoded_user_pass = base64.b64encode(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        #user = crawler.settings.get('HTTP_PROXY_USER')
        #passwd = crawler.settings.get('HTTP_PROXY_PASSWD')
        #if not user or not passwd:
        #    raise NotConfigured
        # http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
        #user = "newbie"
        #passwd = "pE5-Xtv#fS5McU6I"
        #creds = self._basic_auth_header(user, passwd)
        #request.headers['Proxy-Authorization'] = b'Basic ' + creds



class MytestDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        print ("in-------------------------------2")
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

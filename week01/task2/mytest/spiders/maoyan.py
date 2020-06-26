# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from mytest.items import MytestItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board']

    def start_requests(self):
        yield scrapy.Request(url="https://maoyan.com/board", callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath('//dd')
        for movie in movies:
            print ("-----------------------------------")
            item = MytestItem()
            name = movie.xpath('./a/@title').get().strip()
            url = "https://maoyan.com" + movie.xpath('./a/@href').get().strip()
            releasetime = movies.xpath('./div/div/div[1]/p[3]/text()').get().strip()
            item['name'] = name
            item['url'] = url
            item['releasetime'] = releasetime.split("：")[-1]
            print(name,url)
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        film_type = Selector(response=response).xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a/text()').getall()
        for i in range(0,len(film_type)):
            film_type[i] = film_type[i].strip()
        item['film_type'] = " ".join(film_type)
        yield item

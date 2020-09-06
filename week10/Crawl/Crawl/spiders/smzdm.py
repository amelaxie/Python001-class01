# -*- coding: utf-8 -*-
import scrapy
import json
from Crawl.items import GoodsItem, CommentItem
from scrapy.selector import Selector
import datetime
import re


def convert_time(display_time):
    nowtime = datetime.datetime.now()
    if display_time == '刚刚':
        return nowtime.strftime('%Y-%m-%d %H:%M:%S')
    elif display_time.find("分钟前") != -1:
        minute = int(display_time.replace("分钟前", ""))
        return (nowtime - datetime.timedelta(minutes=minute)).strftime('%Y-%m-%d %H:%M:%S')
    elif display_time.find("小时前") != -1:
        hour = int(display_time.replace("小时前", ""))
        return (nowtime - datetime.timedelta(hours=hour)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        pattern_short_date = "^([0-1][0-9]\-[0-3][0-9] [0-2][0-9]\:[0-5][0-9])$"
        pattern_fulll_date = "^[0-9]{4}\-([0-1][0-9]\-[0-3][0-9] [0-2][0-9]\:[0-5][0-9]\:[0-5][0-9])$"
        short_date = re.search(pattern_short_date, display_time)
        full_date = re.search(pattern_fulll_date, display_time)
        if short_date:
            time = f"{nowtime.strftime('%Y')}-{short_date.group(1)}:00"
            return time
        elif full_date:
            return display_time
        else:
            return None


class SmzdmSpider(scrapy.Spider):
    name = 'smzdm'
    allowed_domains = ['www.smzdm.com']
    start_urls = ['http://www.smzdm.com/']

    def start_requests(self):
        yield scrapy.Request(url="https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/",
                             callback=self.parse_ranking)

    # 爬取排行榜每页信息
    def parse_ranking(self, response):
        try:
            # 如果有下一页继续爬取
            next_page = Selector(response=response).xpath('//li[@class="page-turn  next-page"]/a/@href').get()
            if next_page:
                yield scrapy.Request(url=next_page.strip(), callback=self.parse_ranking)
            # 循环爬取每个商品信息
            goods_list = Selector(response=response).xpath('//ul[@class="feed-list-hits"]/li')
            for goods_content in goods_list:
                item = GoodsItem()
                goods_info = goods_content.xpath(
                    './div/div[@class="z-feed-content "]/div[@class="z-feed-foot"]/div[@class="z-feed-foot-r"]/div/div/a[@class="z-btn z-btn-red"]/@onclick').get().strip()
                # 临时将详情页存入url字段
                item['url'] = goods_content.xpath(
                    './div/div[@class="z-feed-content "]/div[@class="z-feed-foot"]/div[@class="z-feed-foot-l"]/a[2]/@href').get().strip()
                display_time = goods_content.xpath(
                    './div/div[@class="z-feed-content "]/div[@class="z-feed-foot"]/div[@class="z-feed-foot-r"]/span[@class="feed-block-extras"]/text()').get().strip()
                item['time'] = convert_time(display_time)
                pattern = ".*dataLayer.push.*gtmAddToCart\((.*?)\)$"
                info_text = re.search(pattern, goods_info)
                if info_text:
                    goods_json = json.loads(info_text.group(1).replace("'", '"'))
                    item['name'] = goods_json["name"]
                    item['goods_id'] = goods_json['id']
                    item['brand'] = goods_json['brand']
                    item['category'] = goods_json['category']
                    item['price'] = goods_json['price']
                    yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parse_comment)
        except Exception as e:
            print(f"抓取榜单页面时出现错误：{str(e)}")

    # 爬取商品详情页信息和评论信息
    def parse_comment(self, response):
        try:
            worth = Selector(response=response).xpath('//span[@id="rating_worthy_num"]/text()').get()
            worthless = Selector(response=response).xpath('//span[@id="rating_unworthy_num"]/text()').get()
            price = Selector(response=response).xpath('//div[@class="price"]/span/text()').get()
            url = Selector(response=response).xpath('//a[@class="img-box"]/img[@class="main-img"]/@src').get()
            if not price:
                price = Selector(response=response).xpath('//div[@class="old-price-box"]/p/span[2]/text()').get()
            goods_item = response.meta['item']
            goods_item['visible_price'] = price
            goods_item['worth'] = worth
            goods_item['worthless'] = worthless
            goods_item['url'] = url
            yield goods_item  # 返回商品ITEM
            comment_list = Selector(response=response).xpath('//ul[@class="comment_listBox"]/li[@class="comment_list"]')
            for comment_content in comment_list:
                item = CommentItem()
                item['goods_id'] = goods_item['goods_id']
                item['comment_id'] = comment_content.xpath('./@id').get().strip().split("_")[-1]
                display_time = comment_content.xpath(
                    './div[@class="comment_conBox"]/div[@class="comment_avatar_time "]/div[@class="time"]/text()').get().strip()
                item['time'] = convert_time(display_time)
                item['text'] = comment_content.xpath(
                    './div[@class="comment_conBox"]/div[@class="comment_conWrap"]/div[@class="comment_con"]/p/span/text()').get()
                if item['text']:
                    if item['text'] != " ":
                        yield item  # 返回评论ITEM
            # 检查评论是否有下一页，如果有继续爬取
            next_page = Selector(response=response).xpath(
                '//*[@class="pagination"]/li[@class="pagedown"]/a/@href').get()
            if next_page:
                yield scrapy.Request(url=next_page.strip(), meta={'item': goods_item}, callback=self.parse_comment)
        except Exception as e:
            print(f"抓取评论页面时出现错误：{str(e)}")

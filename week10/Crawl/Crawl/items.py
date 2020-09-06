# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodsItem(scrapy.Item):
    goods_id = scrapy.Field()   # 商品id
    name = scrapy.Field()       # 商品名称
    brand = scrapy.Field()      # 品牌
    category = scrapy.Field()   # 商品分类
    price = scrapy.Field()      # 价格
    url = scrapy.Field()        # 图片地址
    visible_price = scrapy.Field()  # 页面显示价格可能含中文
    worth = scrapy.Field()      # 值
    worthless = scrapy.Field()  # 不值
    time = scrapy.Field()       # 发布时间
    update_time = scrapy.Field()    # 更新时间


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field() # 评论id
    goods_id = scrapy.Field()   # 商品id
    text = scrapy.Field()       # 评论内容
    time = scrapy.Field()       # 评论时间

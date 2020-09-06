# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, DateTime, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Crawl.items import GoodsItem, CommentItem

Base = declarative_base()


# 商品数据模型
class GoodsModel(Base):
    __tablename__ = 't_goods'
    goods_id = Column(Integer, primary_key=True)  # 商品id
    brand = Column(String(64))  # 品牌
    category = Column(String(64))  # 分类
    price = Column(Integer)  # 价格
    name = Column(String(512))  # 商品名称
    url = Column(String(160))  # 图片地址
    visible_price = Column(String(64))  # 显示价格
    worth = Column(Integer)  # 值
    worthless = Column(Integer)  # 不值
    time = Column(DateTime)  # 发布时间
    update_time = Column(TIMESTAMP(True), nullable=False, server_default=func.now(), onupdate=func.now())  # 更新时间

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


# 评论数据模型
class CommentModel(Base):
    __tablename__ = 't_comment'
    comment_id = Column(Integer, primary_key=True)  # 评论id
    goods_id = Column(Integer)  # 商品id
    text = Column(String(1024))  # 评论内容
    time = Column(DateTime)  # 评论时间
    update_time = Column(TIMESTAMP(True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class CrawlPipeline:
    def process_item(self, item, spider):
        return item


# 存储到mysql的pipeline
class MySQLPipeline(object):
    def __init__(self):  # 执行爬虫时
        try:
            self.engine = create_engine('mysql+pymysql://spider:mydb999@localhost:3306/spider?charset=utf8mb4',
                                        echo=False)
            self.DbSession = sessionmaker(bind=self.engine)
            self.dbsession = self.DbSession()
            # 如果没有建表，将初始化表
            if GoodsModel.__tablename__ not in self.engine.table_names() or \
                    CommentModel.__tablename__ not in self.engine.table_names():
                Base.metadata.create_all(self.engine)
        except Exception as e:
            print("初始化数据库时发生错误")
            print(e)

    def process_item(self, item, spider):  # 爬取过程中执行的函数
        try:
            # 判断item类型，根据不同类型进行处理存储
            if isinstance(item, GoodsItem):
                if self.dbsession.query(GoodsModel).filter(GoodsModel.goods_id == item["goods_id"]).first() is None:
                    self.dbsession.add(GoodsModel(**item))
                    self.dbsession.commit()
            elif isinstance(item, CommentItem):
                if self.dbsession.query(CommentModel).filter(
                        CommentModel.comment_id == item["comment_id"]).first() is None:
                    self.dbsession.add(CommentModel(**item))
                    self.dbsession.commit()
        except Exception as e:
            self.dbsession.close()
            print("存储数据时发生错误")
            print(e)

    def close_spider(self, spider):  # 关闭爬虫时
        self.dbsession.close()

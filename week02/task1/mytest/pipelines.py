# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class MovieTemplate():
    id = Column(Integer, primary_key=True)  # 主键自增
    name = Column(String(100))
    url = Column(String(100))
    releasetime = Column(String(100))
    film_type = Column(String(100))

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class MytestPipeline:
    def process_item(self, item, spider):
        name = item['name']
        # url = item['url']
        releasetime = item['releasetime']
        film_type = item['film_type']
        with open("./movies.csv", "a+", encoding="utf-8") as f:
            output = f'|{name}|\t|{film_type}|\t|{releasetime}|\n\n'
            f.write(output)
        return item

# 存储到mysql的pipeline
class MySQLPipeline(object):
    def __init__(self):  # 执行爬虫时
        try:
            self.engine = create_engine(
                'mysql://spider:mydb999@localhost:3306/spider?charset=utf8', echo=True)  # 连接数据库
            self.DbSession = sessionmaker(bind=self.engine)
            self.dbsession = self.DbSession()
            Base = declarative_base()
            # Base.metadata.create_all(self.engine)
            #动态创建orm类,必须继承Base, 这个表名是固定的,如果需要为每个爬虫创建一个表,请使用process_item中的
            self.Movie = type('test_movie', (Base, MovieTemplate), {
                              '__tablename__': 't_movies'})
        except Exception as e:
            print("初始化数据库时发生错误")
            print(e)

    def process_item(self, item, spider):  # 爬取过程中执行的函数
        try:
            # 按照爬虫名动态创建一个类
            # if not hasattr(self,spider.name):
            #     self.Movie = type(spider.name, (Base, MovieTemplate), {'__tablename__': spider.name, })
            # 在数据库中创建这个表
            if spider.name not in self.engine.table_names(): #create table for this spider
                self.Movie.metadata.create_all(self.engine)

            self.dbsession.add(self.Movie(**item))
            self.dbsession.commit()
        except Exception as e:
            print("存储数据时发生错误")
            print(e)

    def close_spider(self, spider):  # 关闭爬虫时
        self.dbsession.close()


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MytestPipeline:
    def process_item(self, item, spider):
        name = item['name']
        # url = item['url']
        releasetime = item['releasetime']
        film_type  = item['film_type']
        with open("./movies.csv", "a+", encoding="utf-8") as f:
            output  = f'|{name}|\t|{film_type}|\t|{releasetime}|\n\n'
            f.write(output)
        return item

# -*- coding: utf-8 -*-
import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhilianspiderPipeline(object):

    def __init__(self):
        #配置mongodb
        self.client = pymongo.MongoClient("localhost", connect=False)
        db = self.client["zhilian"]
        #self.collection = db["python_guangzhou"]
        self.collection = db["python"]

    def process_item(self, item, spider):
        content = dict(item)
        self.collection.insert(content)
        print("###################抓取数据已经存入MongoDB########################")
        return item

    def close_spider(self, spider):   #在关闭爬虫的时候会被调用
        self.client.close()


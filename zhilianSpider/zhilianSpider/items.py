# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    job_name = scrapy.Field()    #工作名称
    job_link = scrapy.Field()    #工作连接
    job_info = scrapy.Field()    #工作描述
    job_tags = scrapy.Field()    #工作福利等

    company = scrapy.Field()     #公司名称
    address = scrapy.Field()     #公司地址
    salary = scrapy.Field()      #工资

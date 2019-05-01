# -*- coding: utf-8 -*-
import scrapy
from ..items import ZhilianspiderItem
from bs4 import BeautifulSoup

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['m.zhaopin.com']
    # start_urls = ['https://m.zhaopin.com/hangzhou/']
    #https://m.zhaopin.com/guangzhou-763/?keyword=python&order=0&maprange=3&ishome=0
    start_urls = ['https://m.zhaopin.com/beijing-530/?keyword=python&pageindex=1&maprange=3&islocation=0']
    base_url  = 'https://m.zhaopin.com/'
    def parse(self, response):
        print(response.url)
        # 这里是body 而不是text
        soup = BeautifulSoup(response.body,'lxml')
        all_sec = soup.find('div',class_='r_searchlist positiolist').find_all('section')
        for sec in all_sec:
            d_link = sec.find('a',class_='boxsizing')['data-link']
            detail_link = self.base_url+d_link
            if detail_link:
                yield scrapy.Request(detail_link,callback=self.parse_detail)

        # 是否有下一页的链接
        if soup.find('a',class_='nextpage'):
            next_url = self.base_url+soup.find('a',class_='nextpage')['href']
            print('next_url  ',next_url)
            # 若果有重复的，则不进行过滤
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)


    def parse_detail(self,response):
        item = ZhilianspiderItem()
        item['job_link'] = response.url
        item['job_name'] = response.xpath('//*[@class="job-name fl"]/text()')[0].extract()
        item['company'] = response.xpath('//*[@class="comp-name"]/text()')[0].extract()
        item['address'] = response.xpath('//*[@class="add"]/text()').extract_first()
        item['job_info'] = ''.join(response.xpath('//*[@class="about-main"]/p/text()').extract())
        item['salary'] = response.xpath('//*[@class="job-sal fr"]/text()')[0].extract()
        item['job_tags'] = ';'.join(response.xpath("//*[@class='tag']/text()").extract())
        yield item

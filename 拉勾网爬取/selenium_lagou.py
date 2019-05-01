# -*- coding: utf-8 -*-
# 爬取职位信息，通过selenium来模拟浏览器

from selenium import webdriver
from lxml import etree
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LagouSpider:
    driver_path = 'C:\Program Files (x86)\Google\chromedriver_win32\chromedriver.exe'

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.positions = []

    # 打开拉钩python职位页面
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source  # 每一页的HTML代码
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="pager_container"]/span[last()]'))
            )
            self.parse_list_page(source)
            next_btn = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')  # 下一页标签
            if 'pager_next pager_next_disabled' in next_btn.get_attribute('class'):  # 到最后一页就退出
                break
            else:
                next_btn.click()  # 点击下一页
            time.sleep(1)

    # 解析职位url
    def parse_list_page(self, source):
        html = etree.HTML(source)
        urls = html.xpath('//a[@class="position_link"]/@href')  # 职位详情页url
        for url in urls:
            self.request_detail_page(url)
            time.sleep(1)

    # 打开职位详情页面
    def request_detail_page(self, url):
        self.driver.execute_script('window.open("{}")'.format(url))  # 职位详情页面需要打开一个新的页面
        self.driver.switch_to_window(self.driver.window_handles[1])  # 切换到职位详情页
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='job-name']/span[@class='name']"))
        )
        source = self.driver.page_source
        self.parse_detail_page(source)
        self.driver.close()  # 关闭当前职位详情页面
        self.driver.switch_to_window(self.driver.window_handles[0])  # 切换回职位页

    # 解析职位信息
    def parse_detail_page(self, sourse):
        html = etree.HTML(sourse)
        position_name = html.xpath("//span[@class='name']/text()")[0]  # 职位名称
        company_name = html.xpath('//h2[@class="fl"]/text()')[0].strip()  # 公司名称
        job_request_spans = html.xpath("//dd[@class='job_request']//span")
        salary = job_request_spans[0].xpath('.//text()')[0].strip()  # 薪水
        city = job_request_spans[1].xpath(".//text()")[0].strip()  # 城市
        city = re.sub(r"[\s/]", "", city)
        work_years = job_request_spans[2].xpath(".//text()")[0].strip()  # 工作年限
        work_years = re.sub(r"[\s/]", "", work_years)
        education = job_request_spans[3].xpath(".//text()")[0].strip()  # 学历
        education = re.sub(r"[\s/]", "", education)
        desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()  # 职位描述

        position = {
            'name': position_name,
            'company_name': company_name,
            'salary': salary,
            'city': city,
            'work_years': work_years,
            'education': education,
            'desc': desc
        }
        self.positions.append(position)
        print(position)
        print('='*40)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()
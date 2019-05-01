# -*- coding: utf-8 -*-
#Requests+正则表达式
import requests
from requests.exceptions import RequestException
import re
import json
import time
import csv

# 1.目标网站：http://maoyan.com/board/4?offset=0
# 2.获取单页源代码，用requests，为了使我们的程序在请求时遇到错误，可以捕获这种错误RequestException:，就要用到try…except方法
#
def get_one_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0(WindowsNT6.3;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36"
        }
        # 判断响应是否成功,若成功打印响应内容,否则返回None
        res = requests.get(url,headers=headers)
        content = res.text
        if res.status_code == 200:
            return content
        else:
            return None
    except RequestException:
        return None

# 3.解析获取的单页源代码，使用正则匹配需要的内容，在通过遍历方式提取信息，输出字典键值对
#
def parse_one_url(html):
    regular = '<dd>.*?board-index.*?>(\d+)</i>.*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?score.*?integer">(.*?)</i>.*?>(.*?)</i>.*?</dd>'
    pattren = re.compile(regular,re.S)
    items = re.findall(pattren,html)
    #print(items)
    #遍历方式提取信息，输出字典键值对
    for item in items:
        yield{
           '排名' : item[0],
            '电影名称' : item[1],
            '主演' : item[2].strip()[3:],
            '上映时间、地区' : item[3][5:],
            '总评分' : item[4]+item[5]
        }

# 4.将抓去内容保存在本地文件（.txt/.csv等）或数据库
#
def save_to_txt(item):
    #保存到txt文件
    with open('maoyan.txt','a',encoding="utf-8") as f:
        # 利用json.dumps()方法将字典序列化,并将ensure_ascii参数设置为False,保证结果是中文而不是Unicode码.
        f.write(json.dumps(item,ensure_ascii=False) + '\n')
        f.close()

def write_to_csvField(fieldnames):
    '''写入csv文件字段'''
    with open("maoyan1.csv", 'a', encoding='utf-8', newline='') as f:
        #将字段名传给Dictwriter来初始化一个字典写入对象
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        #调用writeheader方法写入字段名
        writer.writeheader()

def write_to_csvRows(movie_list,fieldnames):
    '''写入csv文件内容'''
    with open("maoyan1.csv",'a',encoding='utf-8',newline='') as f:
        #将字段名传给Dictwriter来初始化一个字典写入对象
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        #调用writeheader方法写入字段名
        #writer.writeheader()            ###这里写入字段的话会造成在抓取多个时重复.
        writer.writerows(movie_list)
        f.close()

# 5.分析url变化并实现多页爬取
#url = "http://maoyan.com/board/4?offset={}".format(page)
#main(page=i*10)

def main(page):
    url = "http://maoyan.com/board/4?offset={}".format(page)
    html = get_one_url(url)
    movie_list = []
    for item in parse_one_url(html):
        #save_to_txt(item)
        movie_list.append(item)
    print(movie_list)
    write_to_csvRows(movie_list, fieldnames)


if __name__ == '__main__':
    start = time.clock()
    # 将字段名传入列表
    fieldnames = ["排名", "电影名称", "主演", "上映时间、地区", "总评分"]
    write_to_csvField(fieldnames)
    for i in range(10):
        main(page=i*10)
    end = time.clock()
    print("********************************************")
    print("猫眼top100电影信息已经爬取完毕,总用时为%s"%(end-start))
    print("********************************************")
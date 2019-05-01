# coding=utf-8
# 方式一：scrapy crawl zhilian
# 方式二（建议）：创建一个run.py 文件，然后运行python run.py

#执行scrapy.cmdline中的execute
from scrapy.cmdline import execute
#sys模块包含了与Python解释器和它的环境有关的函数
import sys
# os模块包含普遍的操作系统功能，与具体的平台无关
import os

sys.path.append(os.path.join(os.getcwd()))

crawlline = 'zhilian'
# crawlline = ''

execute(['scarpy','crawl',crawlline])
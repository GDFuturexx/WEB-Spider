import requests
import base64
import re
from bs4 import BeautifulSoup
import threading
import hashlib
import math
import lxml


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}

# 解析加密img图片的方法,返回真实imgurl地址列表
def parse_img_url(pages):
    print('parse_img_url start')
    real_img_url = []  # 真实img地址
    for i in pages:
        # 使用BeautifulSoup解析为xml形式,方便查找html节点
        soup = BeautifulSoup(i, 'lxml')
        # 根据class属性值查找加密的imgurl所在
        imgurl = soup.find_all(class_='img-hash')
        for j in imgurl:
            # 转为真实地址
            url = j.text
            url = base64.b64decode(url).decode('utf-8')
            real_img_url.append(url)
        print('parse_img_url end')
        return real_img_url

# 下载图片的方法
# suffix和url_dase64是为了命名而存在
def downloadimg(url, header):
    print('downloadimg start', url)
    # 利用hashlib生成文件名
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    filename = md5.hexdigest()
    print('filename:', filename, '\n', 'type;', type(filename))
    # 补全url
    url = 'http:' + url
    # 提取文件后缀
    suffix = url.split('.')
    suffix = suffix[len(suffix) - 1]

    # 抓取页面
    response = requests.get(url, header)
    img = response.content
    with open('./xxoo/' + filename + '.' + suffix, 'wb') as f:
        f.write(img)
    print('下载成功')

# 自定义线程类
class Spider(threading.Thread):
    print('main.header:',header)
    count=1
    def __init__(self, pages):
        threading.Thread.__init__(self)  # 初始化线程
        self.pages = pages
        print('创建线程', Spider.count)
        Spider.count += 1

    def run(self):
        real_img_url = parse_img_url(self.pages)
        # 下载图片
        for url in real_img_url:
            downloadimg(url, header)


# 主程序
def main(amount):
    print('main start')

    # 当前页面
    current_url = 'http://jandan.net/ooxx'

    """
    多线程抓取页面
    """
    pages = []  # 所有待抓取页面
    threads = []  # 所有工作线程
    try:
        for i in range(amount):
            current_page = requests.get(current_url, headers=header).text  # 当前页源码
            pages.append(current_page)
            current_url = 'http:' + re.search(r'.*Older\sComments\"\shref=\"(.*?)\"\sclass.*', current_page).group(1)  # 提取下个页面url
    except Exception as e:
        print('错误', e)
        pass
    t_amount = 10 if len(pages) > 10 else len(pages)  # 页面抓取线程数,最大为10
    for i in range(t_amount):
        # 下方长长的部分,是把查询内容均分为符合生成的线程数量的方式.如线程10,任务为23个页面,就将23个页面均分为10份交与线程处理
        t = Spider(pages[math.ceil(int((len(pages)) / t_amount) * i):math.ceil(int((len(pages)) / t_amount) * (i + 1))])
        threads.append(t)  # 放入生成的线程,布置工作
        # 开始工作
        print('线程池数量,', len(threads))
    for t in threads:
        print(t.name)
        t.start()
    print('下载成功!')

if __name__ == '__main__':
    amount = input('请输入抓取页数后按回车开始(小于100），从首页开始计数):')
    main(int(amount))  # 抓取首页开始的前amount页的图片
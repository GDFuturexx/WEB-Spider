##把代码整理一下，实现保存功能，并没有解决网站的反爬虫
# coding=utf-8
import requests
from lxml import etree
import os


class mzitu():

    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def all_url(self, url):
        res = self.request(url)##调用request函数把套图地址传进去会返回给我们一个response
        html = etree.HTML(res.text)
        all_a = html.xpath('//div[@class="all"]//ul[@class="archives"]//a')
        for a in all_a:
            title = a.xpath('./text()')  # 取出a标签的文本
            print(u'开始保存：', title)
            path = str(title).replace("?", '_') ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            self.mkdir(path) ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            href = a.xpath('./@href')  # 取出a标签的href属性
            self.html(href) ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！

    def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
        res_html = self.request(href[0])
        self.headers['referer'] = href[0]
        html_href = etree.HTML(res_html.text)
        max_span = html_href.xpath("//div[@class='pagenavi']/a[last()-1]/span/text()")[0]
        for page in range(1, int(max_span) + 1):
            page_url = href[0] + '/' + str(page)
            self.img(page_url) ##调用img函数

    def img(self, page_url): ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_Soup = etree.HTML(img_html.text)
        img_url = img_Soup.xpath("//div[@class='main-image']//img/@src")[0]
        self.save(img_url)

    def save(self, img_url): ##这个函数保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path): ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("D:\mzitu", path))
            os.chdir(os.path.join("D:\mzitu", path)) ##切换到目录
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def request(self, url): ##这个函数获取网页的response 然后返回
        content = requests.get(url, headers=self.headers)
        return content

Mzitu = mzitu() ##实例化
Mzitu.all_url('http://www.mzitu.com/all') ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
print("*************finish**************")
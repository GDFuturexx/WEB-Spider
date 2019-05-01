##实现获取所有下载图片地址
import requests
from lxml import etree

all_url='https://www.mzitu.com/all'
headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    }
res = requests.get(all_url,headers=headers)
content = res.text

html = etree.HTML(content)

all_alist = html.xpath('//div[@class="all"]//ul[@class="archives"]//a')

for a in all_alist:
    title = a.xpath('./text()') #取出a标签的文本
    href = a.xpath('./@href') #取出a标签的href属性
    # print(href)
    res_html = requests.get(href[0],headers=headers)
    # print(res_html)
    html_href = etree.HTML(res_html.text)
    max_span = html_href.xpath("//div[@class='pagenavi']/a[last()-1]/span/text()")[0]
    # print(max_span)
    for page in range(1, int(max_span) + 1):
        # print(type(page))
        page_url = href[0] + '/' + str(page)
        # print(page_url)  ##这个page_url就是每张图片的页面地址啦！但还不是实际地址！
        img_html = requests.get(page_url, headers=headers)
        img_Soup = etree.HTML(img_html.text)
        img_url = img_Soup.xpath("//div[@class='main-image']//img/@src")[0]
        print(img_url)



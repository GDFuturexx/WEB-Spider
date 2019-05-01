import requests
import re
import json

# def basic(page):
query = input("请输入你需要搜索的内容：")
s = 0   #s=（i-1）*44
# 模拟浏览器发送http请求
# 伪造http请求

url = "https://s.taobao.com/search?q={}&p4ppushleft=1%2C48&s={}".format(query,s)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    "cookie" : "thw=cn; cna=VD/sE21OFX4CATo+Hz34/RWt; t=196a0d6ae2fe84140fff845e8d10a545; miid=95609471510316280; tracknick=hhgx21; tg=0; hng=CN%7Czh-CN%7CCNY%7C156; enc=dQyD0aT1FWDkQYj3Bod4McGUgjVSZkHV2ZVbqZvQx%2B5MKemd2lzsYFRtLLsf9we%2FRRii3v3Fg2ipwVw9h%2Fb1RQ%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=16593c1792210e-0ee4c74c74a73a-9393265-100200-16593c179235e5; _cc_=W5iHLLyFfA%3D%3D; v=0; cookie2=2b60525e4f4751545e907923f0e6c0d9; _tb_token_=5e535ebf5838; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; isg=BI2N2Bw66qoUFk4w4vzBjtQ_nKnHwsmHpbSKys8SySSTxq14l7rRDNtUNBoFHdn0; JSESSIONID=9DAB9E44B975A712F8B4D7C97A1F2888'"
}

response = requests.get(url,headers=headers)
res = response.text
# print(res)
data = re.findall(r'g_page_config = (.*?)g_srp_loadCss',res,re.S)[0]
data = data.strip(' \n;')       # 去掉其他字符,去掉首尾的空格换行和分号这里是
data = json.loads(data)    #json转换成字典
# 在字典拿出我们需要的信息,所有商品信息，这个一个列表
data = data['mods']['itemlist']['data']['auctions']
# print(len(data))  #打印一下这个列表长度，确认不为空


# 数据持久化（写数据库，写文件）
# csv文件   可以同excel打开
f = open('淘宝搜索{}所得数据.csv'.format(query),'w',encoding='utf-8')
# 写表头
f.write('标题,标价,购买人数,是否包邮,是否天猫,地区,店名,url\n')
for item in data:
    temp ={
        'title':item['title'],
        'view_price':item['view_price'],
        'view_sales':item['view_sales'],
        'view_fee':'否' if float(item['view_fee']) else '是',
        'isTmall':'是' if item['shopcard']['isTmall'] else '否',
        'area':item['item_loc'],
        'name':item['nick'],
        'detail_url':item['detail_url']
    }
    f.write(('{title},{view_price},{view_sales},{view_fee},{isTmall},{area},{name},{detail_url}\n').format(**temp))
f.close()

# if __name__ == '__main__':
#     for i in range(1,101):
#      basic(page=(i-1)*44)

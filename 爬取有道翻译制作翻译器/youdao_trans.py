# urllib提供了一系列用于操作URL的功能,Urllib是python内置的HTTP请求库,
# urllib.request是请求模块,urllib.parse是解析模块
import urllib.request,urllib.parse,json

content = input('请输入要翻译的内容：')

# url就是Request URL:的数据
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

# data是一个字典，里面是Form Data的数据
data = {}
data['i'] = content
# data['from'] = 'AUTO'
# data['to'] = 'AUTO'
# data['smartresult'] = 'dict'
# data['client'] = 'fanyideskweb'
# data['salt'] = '1539143000896'
# data['sign'] = '77a0b05cd09c3f6cc15bbba18106d051'
data['doctype'] = 'json'
# data['version'] = '2.1'
# data['keyfrom'] = 'fanyi.web'
# data['action'] = 'FY_BY_REALTIME'
# data['typoResult'] = 'false'

# 把data数据进行编码解析，然后再赋值给data覆盖掉之前的data
data = urllib.parse.urlencode(data).encode('utf-8')  # encode就是把unicode（python是unicode编码）变成其他编码格式

res = urllib.request.Request(url,data,headers)
response = urllib.request.urlopen(res)
# decode就是把其他编码格式解析成unicode编码格式
# python unicode 编码的中文输出 decode('unicode-escape')
html = response.read().decode('utf-8')

# print(html)
target = json.loads(html)
print("翻译结果为: %s" % (target['translateResult'][0][0]['tgt']))
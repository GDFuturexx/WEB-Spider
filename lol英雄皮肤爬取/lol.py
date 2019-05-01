import requests
import re
import json
import time

# 获取js源代码 获取英雄id
# 拼接url地址
# 获取下载图片地址
# 下载图片

# 驼峰命名法
# 注释

def getLOLimages():
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 69.0.3497.100Safari / 537.36'
    }
    url_js = 'http://lol.qq.com/biz/hero/champion.js'
    # text获取的是字符串str；content或取的是bytes字节，所获取内容前面有个b，不能直接用，需要转码
    res_js = requests.get(url_js,headers=headers).content
    # 转码，转成字符串
    html_js = res_js.decode()
    # 正则表达式
    req = '"keys":(.*?),"data"'
    list_js = re.findall(req,html_js)
    # print(list_js)
    # print(list_js[0])
    # 字符串str类型转换成字典dict
    dict_js = json.loads(list_js[0])

    # 定义一个图片列表,所有图片地址拼接好的都放在这个列表里
    pic_list = []
    # 循环这个字典,key就是每一个id
    for key in dict_js:
        # key每个英雄对应的id
        # print(key)
        # 循环1到19的数字，应该没有英雄皮肤超过19个的
        for i in range(20):
            # 把数字转换成str字符串才能用len（）计算长度
            # 因为整数没有长度，和整数不能和字符串拼接
            num = str(i)
            if len(num) == 1:
                hero_num = '00' + num
            elif len(num) == 2:
                hero_num ='0' + num
            # 把英雄id的key与皮肤顺序hero_num拼接起来
            numstr = key + hero_num
            # 拼接url地址
            # 其中一个皮肤地址//ossweb-img.qq.com/images/lol/web201310/skin/big103005.jpg
            url = "http://ossweb-img.qq.com/images/lol/web201310/skin/big"+numstr+".jpg"
            # print(url)
            pic_list.append(url)

    # 获取图片的名称
    list_filepath = []
    path = "F:\\Program Files\\feiq\\Recv Files\\python code\\爬虫（正则表达式应用）\\lol英雄皮肤爬取\\lol皮肤\\"
    # dict_js.values()获取dict_js里面的内容
    for name in dict_js.values():
        # 因为名称是名称加数字，不然会覆盖掉，所以这里还要跟上面一致循环
        for i in range(20):
            filepath = path + name + str(i) + '.jpg'
            # 把这些追加到list_filepath列表中
            list_filepath.append(filepath)
            # print(list_filepath)


    # 下载图片
    # 因为list_filepath也是一个列表，要取列表元素，根据下表来取，所以定义一个n
    n = 0
    for picture_url in pic_list:
        res = requests.get(picture_url)
        n = n + 1
        # status_code获取状态码
        # 根据状态码判断图片地址是否为空，因为每个英雄皮肤不定，20只是一个范围
        if res.status_code == 200:
            print('正在下载%s'%list_filepath[n])
            time.sleep(1)  # 每次让他休息一秒再下，防止被封ip
            with open(list_filepath[n],'wb') as f:
                f.write(res.content)




getLOLimages()
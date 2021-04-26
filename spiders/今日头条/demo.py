#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: demo
@time: 2021/4/20
@email: coderflying@163.com
@desc: 
"""
import time

import requests
from urllib.parse import urlencode, urljoin

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive"

}

base_url = 'https://www.toutiao.com/api/pc/feed/?'

category = '__all__'
category = 'news_sports'
params = {
    "max_behot_time": int(time.time()),
    "category": category,
    "utm_source": "toutiao",
    "widen": 1,
    "tadrequire": "true",

}

url = base_url + urlencode(params)
print(url)
_signature = input("请输入")
url += "&" + urlencode({"_signature":_signature})
response = requests.get(url,headers=headers)
print(response.text)
print(response.url)
print(response.json())

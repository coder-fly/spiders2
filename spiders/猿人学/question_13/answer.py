#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/8
@email: coderflying@163.com
@desc: 
"""
import re

import requests

from spiders.猿人学 import get_session


session = get_session()
total = []
html = session.get('http://match.yuanrenxue.com/match/13').text
cookie = ''.join(re.findall(r"\('(\S)'\)", html))

session.cookies.update({
    "yuanrenxue_cookie":cookie.split("=")[1]
})
cookies = session.cookies.get_dict()
headers = {'Host': 'match.猿人学.com',
               'Connection': 'keep-alive',
               'Content-Length': '0',
               'User-Agent': '猿人学.project',
               'Accept': '*/*', 'Origin': 'http://match.yuanrenxue.com',
               'Referer': 'http://match.yuanrenxue.com/match/3', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
for i in range(1,6):
    params = {
        "page":i,
    }
    response = requests.get('http://match.yuanrenxue.com/api/match/13', params=params, cookies=cookies,headers=headers).json()
    total.extend([item['value'] for item in response['data']])

print(sum(total))
# 213133

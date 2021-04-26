#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/3/14
@email: coderflying@163.com
@desc: 
"""
import re
from spiders.猿人学 import get_session
import execjs

with open("udc.js", 'r') as f:
    js = f.read()

session = get_session()
response = session.get('http://match.yuanrenxue.com/match/9')
timestamp = re.search(r"decrypt\('(\d+)'\)", response.text).group(1)
js = js.replace("1615721220",timestamp)
ctx = execjs.compile(js)
cookie_str = ctx.eval("document.cookie")
m = cookie_str.split("=")[1].split("; ")[0]
session.cookies.update({
    "m":m
})
result, count = 0, 0
for i in range(1, 6):
    params = {
        "page":i
    }

    response = session.get('http://match.yuanrenxue.com/api/match/9', params=params).json()
    result += sum([item['value'] for item in response['data']])
    count += len(response['data'])
print(result / count)


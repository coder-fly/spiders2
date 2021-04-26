#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/12
@email: coderflying@163.com
@desc: 
"""
import time
import execjs

from spiders.猿人学 import get_session

with open("kou.js", "r", encoding="utf-8") as f:
    js = f.read()

ctx = execjs.compile(js)


session = get_session()
result = 0
for i in range(1, 6):
    t = int(time.time()) * 1000
    m = ctx.call("btoa", str(t))
    params = {
        "page":i,
        "m":m,
        "t":t,
    }
    response = session.get('http://match.yuanrenxue.com/api/match/16', params=params).json()
    result += sum([item['value'] for item in response['data']])
print(result) # 287383

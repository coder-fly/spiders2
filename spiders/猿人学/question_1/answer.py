#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: demo
@time: 2021/1/5
@email: coderflying@163.com
@desc: 
"""
import execjs

from spiders.猿人学 import get_session

with open("js.js", "r", encoding="utf-8") as f:
    js = f.read()
ctx = execjs.compile(js)
res = ctx.call("res")
session = get_session()
total = []
for i in range(1,6):
    params = {
        "page":i,
        "m":res
    }
    response = session.get('http://match.yuanrenxue.com/api/match/1', params=params).json()
    total.extend([item['value'] for item in response['data']])

print(sum(total) / len(total))

# 4700
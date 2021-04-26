#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/3/11
@email: coderflying@163.com
@desc: 
"""
import execjs

from spiders.猿人学 import get_session

with open("2.js", "r", encoding="utf-8") as f:
    js = f.read()

session = get_session()
ctx = execjs.compile(js)
cookie = ctx.call("get_cookie")


session.get('http://match.yuanrenxue.com/api/match/2')
cookies = {"m":cookie}
session.cookies.update(cookies)
result = 0
for i in range(1, 6):
    params = {
        "page":i
    }

    response = session.get('http://match.yuanrenxue.com/api/match/2', params=params, cookies=cookies).json()
    print(response)
    result += sum([item['value'] for item in response['data']])
print(result) # 248974
#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/5
@email: coderflying@163.com
@desc: 
"""

from spiders.猿人学 import get_session

session = get_session()
res = {}
for i in range(1, 6):
    session.post("http://match.yuanrenxue.com/logo")
    params = {
        "page":i
    }
    response = session.get('http://match.yuanrenxue.com/api/match/3', params=params).json()['data']
    for item in response:
        value = item['value']
        res[value] = res.get(value, 0) + 1

result = max(zip(res.values(), res.keys()))

print(result)
# (7, 8717)
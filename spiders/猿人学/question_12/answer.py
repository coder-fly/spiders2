#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/8
@email: coderflying@163.com
@desc: 
"""
import base64

from spiders.猿人学 import get_session


session = get_session()
total = []
for i in range(1,6):
    params = {
        "page":i,
        "m":base64.b64encode('猿人学{}'.format(i).encode()).decode()
    }
    response = session.get('http://match.yuanrenxue.com/api/match/12', params=params).json()
    total.extend([item['value'] for item in response['data']])

print(sum(total))
# 247082
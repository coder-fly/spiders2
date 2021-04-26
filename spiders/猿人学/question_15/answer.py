#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/11
@email: coderflying@163.com
@desc: 
"""
import subprocess

from spiders.猿人学 import get_session


session = get_session()
total = []
for i in range(1,6):
    params = {
        "page":i,
        "m":subprocess.getoutput('node js2.js')
    }
    response = session.get('http://match.yuanrenxue.com/api/match/15', params=params).json()
    total.extend([item['value'] for item in response['data']])

print(sum(total)) # 219388

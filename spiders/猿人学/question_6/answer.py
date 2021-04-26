#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/6
@email: coderflying@163.com
@desc: 
"""
import time
import subprocess


from spiders.猿人学 import get_session



result = 0

arr_arg = [1, 8, 7, 3, 5, 7, 10, 2, 9, 4]
for i in range(1, 6):
    session = get_session()
    timestamp = int(time.time())* 1000
    maps = []
    maps.append("{}-{}".format(i, timestamp))
    m = subprocess.getoutput('node 6.js {} {}'.format(timestamp,i))
    params = {
        "page": i,
        "m":m,
        "q":"|".join(maps) + "|"
    }
    response = session.get('http://match.yuanrenxue.com/api/match/6', params=params).json()
    result += sum([item['value'] for item in response['data']])

result *= 24

print(result) # 6883344




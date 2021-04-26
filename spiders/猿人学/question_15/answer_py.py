#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer_py
@time: 2021/3/5
@email: coderflying@163.com
@desc: 
"""
import subprocess
import time
import random
from math import floor

import pywasm
from spiders.猿人学 import get_session

runtime = pywasm.load("main.wasm")

session = get_session()
total = []
for i in range(1,6):
    t1 = int(int(time.time()) / 2)
    t2 = int(int(time.time()) / 2 - floor(random.random() * (50) + 1))
    r = runtime.exec("encode", [t1, t2])
    m = '{}|{}|{}'.format(r, t1, t2)
    params = {
        "page":i,
        "m":m
    }
    response = session.get('http://match.yuanrenxue.com/api/match/15', params=params).json()
    total.extend([item['value'] for item in response['data']])

print(sum(total)) # 219388
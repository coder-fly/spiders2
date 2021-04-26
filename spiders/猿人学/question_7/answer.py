#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/5
@email: coderflying@163.com
@desc: 
"""
import re
from base64 import b64decode

from plugins.parse_ttf.parse_ttf import ParseTTFFont
from spiders.猿人学 import get_session




session = get_session()

max_score, user = 0, ''
html = session.get('http://match.yuanrenxue.com/match/7').text
names = eval(re.search(r';let name=(.*?);', html).group(1))

for i in range(1,6):
    params = {
        "page":i
    }
    response = session.get('http://match.yuanrenxue.com/api/match/7', params=params).json()
    data = response['data']
    woff = response['woff']
    fonts = ParseTTFFont(b64decode(woff.encode())).parse_fonts("猿人学")
    for index, item in enumerate(data, 0):
        value = item['value']
        res = re.sub(r'&#x([a-z0-9]*)',lambda x:fonts.get('0x'+x.group(1)), value).replace(" ","")
        if int(res)> max_score:
            max_score = int(res)
            user = names[(i -1) * 10 + index + 1]

print('max_score:{} user:{}'.format(max_score, user))
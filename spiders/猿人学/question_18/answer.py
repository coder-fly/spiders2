#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/3/22
@email: coderflying@163.com
@desc: 
"""
import time
import base64

from Crypto.Cipher import AES

from spiders.猿人学 import get_session


session = get_session()
result = 0

def pkcs7_padding(data):
    if not isinstance(data, bytes):
        data = data.encode()
    pad_len = 8 - (len(data) % 8)
    data += bytes([pad_len] * pad_len)
    return data


def encrypt(key, iv, text):
    text = pkcs7_padding(text.encode('utf-8'))
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return base64.b64encode(cipher.encrypt(text)).decode()


for i in range(1, 6):
    t = int(time.time())
    key = hex(t)[2:] * 2
    iv = hex(t)[2:] * 2
    v = encrypt(key, iv, "{}|201m329,201m328,201d328,201u328,257u22".format(i))
    params = {
        "page":i,
        "t":t,
        "v":v
    }

    response = session.get('http://match.yuanrenxue.com/match/18data', params=params)
    print(response.json())
    for i in response.json()['data']:
        result += i['value']

print(result)
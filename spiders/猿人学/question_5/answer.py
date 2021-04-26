#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/6
@email: coderflying@163.com
@desc:

AES 加密 填充方式位pkcs7

key: 当前时间戳的base64编码
message: 
"""
import base64
import subprocess

from Crypto.Cipher import AES


from spiders.猿人学 import get_session


def pkcs7_padding(data):
    if not isinstance(data, bytes):
        data = data.encode()
    pad_len = 16 - (len(data) % 8)
    data += bytes([pad_len] * pad_len)
    return data


def encrypt(text):
    global key
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pkcs7_padding(text)
    return base64.b64encode(cipher.encrypt(plaintext))

session = get_session()
data = subprocess.getoutput('node m2.js').splitlines()

f = data[0]
key = base64.b64encode(data[1].encode())[:16]

m = data[2]

RM4hZBv0dDon443M = encrypt(data[3]).decode()
cookies = {
    "m": m,
    "RM4hZBv0dDon443M":RM4hZBv0dDon443M
}

params = {
    "page":2,
    "m":data[1],
    "f":f,
}
result = []
for i in range(1,6):
    params = {
        "page":i,
        "m":data[1],
        "f":f,
    }
    response = session.get('http://match.yuanrenxue.com/api/match/5', cookies=cookies, params=params).json()
    result.extend([i['value'] for i in response['data']])
result.sort(reverse=True)
print(sum(result[:5])) # 47313


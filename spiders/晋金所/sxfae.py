#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: main
@time: 2020/12/1
@email: coderflying@163.com
@desc: 晋金所 https://jjbl.sxfae.com/
depend on pycryptodome
一共有三个参数
sign, data, rsaKey
sign的获取：
    翻页数据的json的md5值
    {"page": 1,  "size": 10}
data的获取:
    AES加密
        mode: CBC
        padding: ZeroPadding
        iv: 16位置随机字符串
        key: 16位随机字符串
rsaKey的获取:
    RSA加密
        publicKey: 公钥为服务器返回的固定值，可以直接写死，建议每次开始时请求获取
        key: 为AES加密中的key和iv组成的字符串: "key_" + key + "|iv_" + iv

"""
import base64
from hashlib import md5

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA

zero_padding = lambda s: s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def get_sign(data):
    return md5(data.encode()).hexdigest()


def encrypt(key, iv, text):
    text = zero_padding(text.encode('utf-8'))
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return base64.b64encode(cipher.encrypt(text)).decode()


def get_rsaKey(publicKey, key):
    rsakey = RSA.importKey(publicKey)
    cipher = PKCS1_v1_5.new(rsakey)
    return base64.b64encode(cipher.encrypt(key.encode())).decode()


def crawl(page):
    ciphertext = '''{"page": ''' + str(page) + ''',"size": 10}'''
    sign = get_sign(ciphertext)
    key = 'XyrWHOmkaZEyRWHu'
    iv = "szazgM3zOYCCHWih"
    data = encrypt(key, iv, ciphertext)

    rsa_key = "key_" + key + "|iv_" + iv
    rsa_publickey = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDndDxaow5cmKy0xXU/zYch/0/I
hduhZpfDK5EU/lpIG4VDZxdN/CSsl67InOny3hIBK6T9QAHxjgXqX1W0M96hxigx
fzELPQc/A24KKSUnjbmz90MoSXnFF6eyFJC6ole5i2UdD5qfQC9cU4mXpY48Y0pt
507CONm5PMheAOMlUQIDAQAB
-----END PUBLIC KEY-----
"""
    rsaKey = get_rsaKey(rsa_publickey, rsa_key)

    formdata = {}
    formdata['sign'] = sign
    formdata['data'] = data
    formdata['rsaKey'] = rsaKey
    return formdata


if __name__ == '__main__':
    formdata = crawl(3)
    import requests

    response = requests.post('https://jjbl.sxfae.com/sxfaeApi/801003', json=formdata)
    print(response.json())

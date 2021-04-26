#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: credit
@time: 2020/12/8
@email: coderflying@163.com
@desc: 信用中国(陕西) 黑名单列表页已经详情页采集 http://credit.shaanxi.gov.cn/
"""

import json
import base64
import requests
from Crypto.Cipher import DES


class CreditChina:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36", }

    def __init__(self):
        self.key = b'%Cf9!AMA@7mGXfz6'[:8]
        self.detail_url = 'http://credit.shaanxi.gov.cn/queryItemData.jspx'

    def crawl(self):
        response = requests.post('http://credit.shaanxi.gov.cn/queryCj.jspx', data={
            "ztType": "1",
            "lb": "black",
        }, headers=self.headers)
        json_response = response.json()
        items = json_response['list']
        for item in items:
            data = "{" + '''"id":"{}","lb":"black","ztType":"1","xy010101":"{}"''' .format(item['id'],item['xy010101'])+ "}"
            formdata = {
                "p": self.encrypt(data).decode()
            }
            response = requests.post(self.detail_url, data=formdata, headers=self.headers)
            json_response = response.json()
            item_ = {}
            item_['dataList'] = self.dencrypt(json_response['dataList'])
            item_['list'] = self.dencrypt(json_response['list'])
            yield item_


    def encrypt(self, text):
        cipher = DES.new(self.key, DES.MODE_ECB)
        plaintext = self.pkcs7_padding(text)
        return base64.b64encode(cipher.encrypt(plaintext))

    def dencrypt(self, text):
        cipher = DES.new(self.key, DES.MODE_ECB)
        plaintext = text.replace("[", "").replace("]", "")
        plaintext = base64.b64decode(plaintext.encode())
        plaintext = cipher.decrypt(plaintext)
        return json.loads(self.pkcs7_unpadding(plaintext))

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len] * pad_len)
        return data

    @staticmethod
    def pkcs7_unpadding(data):
        pad_len = data[-1]
        data = data[:-pad_len]
        return data

if __name__ == '__main__':
    credit = CreditChina()
    for i in credit.crawl():
        print(i)
#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: test
@time: 2021/1/22
@email: coderflying@163.com
@desc: https://www.aqistudy.cn/historydata/monthdata.php?city=%E5%8C%97%E4%BA%AC
"""
import json

import execjs
import requests


class AqistudySpider:


    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        with open("js.js", "r") as f:
            js = f.read()
        self.ctx = execjs.compile(js)

    def start(self):
        method = "GETDAYDATA"
        body = {"city": "北京", "month": "201312"}
        data = {
            "hmebd5PRa": self.ctx.call("encrypt", method, body)
        }
        response = self.session.post('https://www.aqistudy.cn/historydata/api/historyapi.php', data=data)
        result = json.loads(self.ctx.call("decrypt", response.text))
        print(result)



if __name__ == '__main__':
    spider = AqistudySpider()
    spider.start()
#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: demo
@time: 2021/4/1
@email: coderflying@163.com
@desc:
npm install pako atob
"""
import hashlib
import re
import execjs
import requests


class LeisuSportsSpider:
    session = requests.session()
    session.headers = {
        "Referer": "https://live.leisu.com/wanchang-20210331",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    }

    def __init__(self):
        with open("js.js", "r") as f:
            js = f.read()
        self.ctx = execjs.compile(js)

    def start(self):
        date = '20210401'
        response = self.session.get('https://static.leisu.com/public/askaliy/askftb/wc-{}.js'.format(
            hashlib.md5(date.encode()).hexdigest()[:12]))
        plaintext = re.search(r'window\[_t19798\[2\]\] =\s*([\S]*?);', response.text).group(1)
        result = self.ctx.call('get_data', plaintext)
        print(result)


if __name__ == '__main__':
    spider = LeisuSportsSpider()
    spider.start()

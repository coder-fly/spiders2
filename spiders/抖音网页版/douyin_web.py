#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: demo
@time: 2021/3/23
@email: coderflying@163.com
@desc: https://www.iesdouyin.com/share/user/66598046050?u_code=15a8l4332&sec_uid=MS4wLjABAAAAgq8cb7cn9ByhZbmx-XQDdRTvFzmJeBBXOUO4QflP96M&did=MS4wLjABAAAA_p7UVl4yf7S8PNp4izOhRhx7jYaqZJ7YbIkx_RFUS_c&iid=MS4wLjABAAAA3civ65DAFmWrvuK9uyopUtUwrDaqaEjWkqGjRALn69C6EFUQdiGp5hosi-1qVDNx&with_sec_did=1&timestamp=1616482502&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin
"""

import requests

class DouyinWebSpider:
    session = requests.session()
    session.headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3904.108 Safari/537.36",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "accept": "application/json",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9"
}
    def start(self):
        # 请参考douyin.js
        signature = requests.get("http://39.106.57.161:7878/").text
        api = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAACV5Em110SiusElwKlIpUd-MRSi8rBYyg0NfpPrqZmykHY8wLPQ8O4pv3wPL6A-oz&count=21&max_cursor={}&aid=1128&_signature={}&dytk='
        url = api.format(0, signature)
        response = self.session.get(url)
        print(response.json())

if __name__ == '__main__':
    spider = DouyinWebSpider()
    spider.start()


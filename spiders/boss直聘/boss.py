#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: boss
@time: 2021/4/28
@email: coderflying@163.com
@desc: 
"""
import os
import re
import warnings
from urllib.parse import urljoin, quote

import execjs
import requests

warnings.filterwarnings(action="ignore")


class BossZhiPinSpider:
    headers = {
        'authority': 'www.zhipin.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    session = requests.session()
    session.headers = headers
    session.verify = False
    proxy = '127.0.0.1:35124'
    session.proxies = {
        # "http":"http://{}".format(proxy),
        # "https":"http://{}".format(proxy),
    }
    script_path = os.path.dirname(__file__)
    base_url = 'https://www.zhipin.com'
    header = '''const canvas = require('canvas');
const jsdom = require("jsdom");
const {JSDOM} = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`, {
    "url": "$url"
});
window = dom.window;
document = window.document;
XMLHttpRequest = window.XMLHttpRequest;
window.navigator = {
    "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
}
const top = {}
top.location = {
    "href":["$url",

    "$url",
    ]
}

atob = window.atob;'''

    footer = '''var getQueryValue = function (e) {
    var t = new RegExp("(^|&)" + e + "=([^&]*)(&|$)");
    var n = window.location.search.substr(1).match(t);
    if (n != null) return unescape(n[2]);
    return null
};
var n = window.location.href;
var f = getQueryValue("seed") || "";
var d = getQueryValue("ts");
var r = getQueryValue("name");
var m = getQueryValue("callbackUrl");
var h = getQueryValue("srcReferer") || "";

var e = (new Date).getTime() + 32 * 60 * 60 * 1e3 * 2;
var t = "";
var n = {};
var r = ABC;
t = (new r).z(f, parseInt(d) + (480 + (new Date).getTimezoneOffset()) * 60 * 1e3);

function getCookie() {
    return t;
}'''

    def start(self, url):
        # 获取每日变化的script文件地址
        response = self.session.get(url, allow_redirects=False)
        location = response.headers.get('location')
        security_url = urljoin(self.base_url, location)
        name = re.search(r'&name=(\S*?)&', location).group(1)
        js_url = 'https://www.zhipin.com/web/common/security-js/{}.js'.format(name)
        content = self.session.get(js_url).text
        content=re.sub(r"(cC=cG\(cC\)[\s\S]*?undefined\)\)\);)", lambda x:x.group(1) + 'var cE="w.zhipin.com";', content)
        fulljs = self.header.replace('$url', security_url) + content + self.footer
        self.ctx = execjs.compile(fulljs)
        __zp_stoken__ = self.ctx.call('getCookie')
        print(__zp_stoken__)
        for i in range(10):
            cookies = {
                "__zp_stoken__": quote(__zp_stoken__),
            }
            self.session.cookies.update(cookies)
            self.session.headers.update({
                "referer": security_url
            })
            response = self.session.get(url)
            if response.url.startswith("https://www.zhipin.com/web/common/security-check.html") :
                __zp_stoken__ = self.ctx.call("getCookie")
                print("faild")
            else:
                print("success")
                print(response.text)
                continue


if __name__ == '__main__':
    boss = BossZhiPinSpider()
    boss.start('https://www.zhipin.com/c101010100-p100109/')

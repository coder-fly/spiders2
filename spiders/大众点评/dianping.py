#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: dazhongdianping
@time: 2020/12/4
@email: coderflying@163.com
@desc: 大众点评字体解析，该网站自定义字体较多，如果每次都人工录入映射表，很繁琐
"""
import requests

from plugins.font_parse.font_parse import FontParser
class Dianping:

    def parse_fonts(self, url):
        content = requests.get(url).content
        fonts = FontParser(content, offset=2, project="dazhong", ocr_always=False,sort=True).parse()
        return fonts

if __name__ == '__main__':
    dianping = Dianping()
    fonts = dianping.parse_fonts('http://s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/e0753a75.woff')
    print(fonts)
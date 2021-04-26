#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: autohome
@time: 2020/12/3
@email: coderflying@163.com
@desc: https://club.autohome.com.cn/bbs/thread/1aac6114218963ff/94262686-1.html
"""
import re
from io import BytesIO

import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup

from fontTools.ttLib import TTFont

fonts_list = [{'cp': [7, 11, 44], 'xy': [], 'value': '和'}, {'cp': [19, 39, 45], 'xy': [], 'value': '近'},
              {'cp': [7, 37, 41, 45], 'xy': [], 'value': '是'}, {'cp': [26], 'xy': [], 'value': '七'},
              {'cp': [13, 39, 43, 47, 53], 'xy': [], 'value': '的'}, {'cp': [47, 67], 'xy': [], 'value': '地'},
              {'cp': [53, 57, 61, 65], 'xy': [], 'value': '着'}, {'cp': [22], 'xy': [], 'value': '大'},
              {'cp': [3, 7, 11], 'xy': [], 'value': '三'}, {'cp': [7, 32, 44, 48, 52, 59, 65], 'xy': [], 'value': '得'},
              {'cp': [39, 51, 57, 63], 'xy': [], 'value': '低'}, {'cp': [60, 95, 102], 'xy': [], 'value': '矮'},
              {'cp': [7, 33], 'xy': [], 'value': '四'}, {'cp': [26, 54, 61], 'xy': [], 'value': '好'},
              {'cp': [17, 21], 'xy': [], 'value': '五'}, {'cp': [7, 42, 46, 56, 60, 66], 'xy': [], 'value': '短'},
              {'cp': [16, 36, 42], 'xy': [], 'value': '坏'}, {'cp': [16, 22], 'xy': [], 'value': '不'},
              {'cp': [29], 'xy': [], 'value': '左'}, {'cp': [11], 'xy': [['35', '20'], ['851', '29'], ['849', '1672'],
                                                                        ['1006', '1669'], ['1014', '1068'],
                                                                        ['1850', '1071'], ['1828', '893'],
                                                                        ['1004', '916'], ['1036', '19'], ['2017', '-5'],
                                                                        ['2015', '-162'], ['32', '-137']],
                                                     'value': '上'},
              {'cp': [31, 43, 47, 54, 58], 'xy': [], 'value': '很'}, {'cp': [10, 17], 'xy': [], 'value': '八'},
              {'cp': [12, 18, 43, 47, 51], 'xy': [], 'value': '呢'}, {'cp': [6, 12, 25], 'xy': [], 'value': '小'},
              {'cp': [28, 35], 'xy': [], 'value': '长'}, {'cp': [11],
                                                         'xy': [['54', '959'], ['919', '935'], ['940', '1692'],
                                                                ['1107', '1694'], ['1115', '968'], ['1998', '943'],
                                                                ['1997', '799'], ['1113', '808'], ['1126', '-266'],
                                                                ['936', '-272'], ['934', '775'], ['41', '807']],
                                                         'value': '十'}, {'cp': [3, 9, 16, 22], 'xy': [], 'value': '六'},
              {'cp': [33, 53, 57, 63], 'xy': [], 'value': '远'}, {'cp': [6, 12, 16, 23], 'xy': [], 'value': '少'},
              {'cp': [37], 'xy': [], 'value': '九'}, {'cp': [7, 24, 30, 40, 44, 48], 'xy': [], 'value': '高'},
              {'cp': [3, 7], 'xy': [], 'value': '二'}, {'cp': [14], 'xy': [], 'value': '下'},
              {'cp': [24, 49], 'xy': [], 'value': '多'}, {'cp': [3], 'xy': [], 'value': '一'},
              {'cp': [26, 30], 'xy': [], 'value': '右'}, {'cp': [33, 38, 43, 48, 53, 58], 'xy': [], 'value': '更'},
              {'cp': [21], 'xy': [], 'value': '了'}]


class AutoHomeSpider:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36", }
    re_font = r"<span style=['\"]font-family: myfont;['\"]>\u{0};</span>"

    def __init__(self):
        self.session = self.get_session()
        self.parser = HTMLParser()

    def get_session(self):
        session = requests.session()
        session.headers = self.headers
        session.verify = False
        return session

    def crawl(self, url):
        item = {}
        response  = self.session.get(url)
        html = response.text
        font_url = "https:" + re.search(r"format\('embedded-opentype'\),url\('([\s\S]*?)'\)", html).group(1)
        fonts = self.parse_fonts(self.session.get(font_url).content)
        html = self.parser.unescape(html)
        soup = BeautifulSoup(html)
        item['content'] = self.decode_html(fonts,soup.select_one('.tz-paragraph').text)
        item['time'] = soup.select_one('.post-handle-publish strong').text
        item['author'] = re.search(r"topicMemberName: '([\s\S]*?)',", html).group(1)
        return item

    def decode_html(self, fonts, html):
        html = html.encode("unicode-escape")
        for glyphname, value in fonts.items():
            code = glyphname.lower()
            html = re.sub(b"\\\\u" + code.encode(), value.encode('unicode-escape'), html)

        return html.decode('unicode-escape')

    @staticmethod
    def parse_fonts(content):
        """
        :param filepath: 请求ttf地址的响应
        :return: 字体字典
        """
        font = TTFont(BytesIO(content))
        glyphnames = font.getGlyphNames()
        unknown_list, fonts = [], {}
        for glyphname in glyphnames[1:]:
            item = {}
            glyph = font['glyf'][glyphname]
            item["cp"] = glyph.endPtsOfContours
            item["glyphname"] = glyphname
            if item['cp'] == [11]:
                item['xy'] = glyph.coordinates[0]
            unknown_list.append(item)
        for font in fonts_list:
            for dom in unknown_list:
                if dom.get("cp") == font.get("cp") and dom.get("cp") != [12]:
                    fonts[dom['glyphname'][3:]] = font.get("value")
                else:
                    if dom.get("cp") == [12]:

                        if int(dom.get("xy")[0][1]) > 200:
                            fonts[dom['glyphname'][3:]] = "十"
                        else:
                            fonts[dom['glyphname'][3:]] = "上"
        return fonts


if __name__ == '__main__':
    print("\\")
    autohome = AutoHomeSpider()
    item = autohome.crawl('https://club.autohome.com.cn/bbs/thread/1aac6114218963ff/94262686-1.html')
    print(item)
#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: answer
@time: 2021/1/19
@email: coderflying@163.com
@desc: 
"""
import re
import base64
from collections import Counter

from plugins.parse_ttf.baidu_ocr import Baidu
from spiders.猿人学 import get_session
from spiders.猿人学.question_8.tools import ImageHandler


session = get_session()
baidu = Baidu()
verify_url = 'http://match.yuanrenxue.com/api/match/8_verify'
results = []
page = 1
while page <= 5:
    try:
        response = session.get(verify_url).json()
        data = re.search(r'base64,([\s\S]*?)"', response.get("html"))
        fonts = re.search(r'请依次点击：---<p>(\S)</p>---<p>(\S)</p>---<p>(\S)</p>---<p>(\S)</p>', response.get("html")).groups()
        content = base64.b64decode(data.group(1))
        image = ImageHandler(content)
        image.run_test()
        # image.image.show()
        result = baidu.accurate_basic_of_pillow(image.image)
        words, answer = [], []
        [ words.extend(list(item['words'].ljust(3," "))) for item in result.json()['words_result']]
        for font in fonts:
            pixel = (words.index(font)// 3) * 300 + 120 + ((words.index(font) % 3 + 1) * 8)
            answer.append(str(pixel))
        params = {
            "page":page,
            "answer":"|".join(answer) + "|"
        }
        response = session.get("http://match.yuanrenxue.com/api/match/8", params=params)
        for i in response.json()['data']:
            results.append(i['value'])
        page += 1
        print(response.json())
    except Exception as e:
        print(e)
        pass
print(results)
counter = Counter(results)
print(counter.get(max(counter)))
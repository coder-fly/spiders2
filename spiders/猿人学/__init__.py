#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: __init__.py
@time: 2021/3/5
@email: coderflying@163.com
@desc: 猿人学爬虫
"""
import requests

def get_session():
    headers = {'Host': 'match.猿人学.com',
               'Connection': 'keep-alive',
               'Content-Length': '0',
               # 'Cookie':"sessionid=yenozzgrng6zhim4gwm1jcii9cdlgch9",
               'User-Agent': '猿人学.project',
               'Accept': '*/*', 'Origin': 'http://match.yuanrenxue.com',
               'Referer': 'http://match.yuanrenxue.com/match/3', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}

    session = requests.session()
    session.headers = headers
    return session
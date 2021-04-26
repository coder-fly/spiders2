#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: __init__.py
@time: 2021/1/11
@email: coderflying@163.com
@desc: 
"""
import pandas as pd
import datetime

df = pd.date_range(end=datetime.datetime.now(), start=(datetime.datetime.now() - datetime.timedelta(days=260))).map(lambda item:item.strftime("%Y-%m")).drop_duplicates(keep="first").tolist()[-7:]
print(df)

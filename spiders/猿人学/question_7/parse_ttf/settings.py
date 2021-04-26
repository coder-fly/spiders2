#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: settings
@time: 2020/11/27
@email: coderflying@163.com
@desc: 
"""
DEBGU = True

# 百度相关参数
# ACCESS_TOKEN获取 http://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu
CLIENT_ID = 'cVtlDGhNSKb4woHtrU7tONtv'
CLIENT_SECRET = 'tTPG3GmutOX8CHLjDetwwyGE78ZrEp2R'
# 建议使用自己的ACCESS_TOKEN
ACCESS_TOKEN = "24.cef9bd8337a4b835ab5f6b2857eb7c90.2592000.1612432976.282335-17157793"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded"
}

# 图片相关参数
FONT_WIDTH = 90 # 单个字体转成图片的宽度
FONT_HEIGHT = 90 # 长度
BASE_BACKGOUND_WIDTH = FONT_WIDTH + 10
BASE_BACKGOUND_HEIGHT = FONT_HEIGHT + 10
WIDTH_PER_LINE = (BASE_BACKGOUND_WIDTH + FONT_WIDTH) // 2
HEIGHT_PER_LINE = (FONT_HEIGHT + BASE_BACKGOUND_HEIGHT) // 2
FONT_NUMS_PER_LINE = 14

# 忽略的字体名
IGNORE_NAMES = ['glyph00000', 'x', '.null', '.notdef']

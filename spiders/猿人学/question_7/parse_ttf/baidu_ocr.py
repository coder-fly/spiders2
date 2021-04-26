#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: baidu_ocr
@time: 2020/11/27
@email: coderflying@163.com
@desc: 
"""
import urllib3
from base64 import b64encode
from io import BytesIO

import requests
from PIL import Image

from .settings import *


urllib3.disable_warnings()

class Baidu(object):
    """learn more https://cloud.baidu.com/doc/OCR/s/zjwvxzrw8"""
    def __init__(self,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,access_token=ACCESS_TOKEN):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url,data=data).json()
        return response.get("access_token")

    def accurate_basic(self,image_content:bytes):
        """
        调用百度接口，识别图片文字
        :param image_content: image -> BytesIO -> base64
        :return:
        """
        image_contents = b64encode(BytesIO(image_content).read())
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'
        params = {
            "access_token":self.access_token
        }
        data = {
            "image":image_contents,
            "detect_direction":False, # 是否检测图像朝向，默认不检测
            "probability":False # 是否返回识别结果中每一行的置信度
        }

        response = requests.post(url,params=params,data=data,headers=headers)
        return response

    def accurate_basic_of_pillow(self,image:Image):
        """
           调用百度接口，识别图片文字
           :param image_content: image -> BytesIO
           :return:
        """
        imgByteArr = BytesIO()
        image.save(imgByteArr,format="PNG")
        image_contents = b64encode(imgByteArr.getvalue())
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'
        params = {
            "access_token": self.access_token
        }
        data = {
            "image": image_contents,
            "detect_direction":False, # 是否检测图像朝向，默认不检测
            "probability":False # 是否返回识别结果中每一行的置信度
        }

        response = requests.post(url, params=params, data=data, headers=headers, verify=False)
        return response


if __name__ == '__main__':
    print(Baidu().get_access_token())
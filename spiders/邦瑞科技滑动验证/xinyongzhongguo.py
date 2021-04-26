#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: 批量获取图片
@time: 2021/1/26
@email: coderflying@163.com
@desc: 
"""
# !usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import random
from io import BytesIO

from PIL import Image

"""
@author: coderfly
@file: xycq
@time: 2021/1/25
@email: coderflying@163.com
@desc: 
"""
import time
import re
import traceback

import numpy as np
from selenium.webdriver import Chrome, ChromeOptions, ActionChains


class Toutiao:

    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = Chrome(chrome_options=options)
        self.driver.maximize_window()
        self.page_init()
        # self.driver.get('https://valbr.bangruitech.com/asValidate?authId=O_awZ_EmHCHvF0F-gPG6Oy3GWktMKwxH&rank=3&signId=168&ts=1611545765959&uuid=DV5B1dhizqtGpLsWrzDheSORZuaQUZzM&vid=4&hashCode=PY2h_mENYR9cmRiDcctq-0xJjRI_MAs8H5dyX4l0yKDdGQQXFfM-ye3LWWE4zepet7dtAAo2ByrAB8ArN7u1ncTQZBy_quMvMun7oZHUBFfQObe7CCKCBq3GmoRQ5pJcYyd0LCDv7G6huq_Aeh18U_gbsF8SCLZO&returnUrl=https://www.xycq.gov.cn/html/query/agree/list.html?navPage=1')

    def page_init(self):
        # self.driver.get('https://www.xycq.gov.cn/html/query/agree/list.html?navPage=1')
        self.driver.get('https://valbr.bangruitech.com/asValidate?authId=O_awZ_EmHCHvF0F-gPG6Oy3GWktMKwxH&rank=4&signId=168&ts=1611743595241&uuid=LRF1To24g0FMpCMCRRFtLd9cQ9w3WWKG&vid=4&hashCode=N4sYIQCAxtF_8iAWR_2bVvKBL7C9JfjwvvLFYIeA0VziFWoK_4D8O6R38bU1RkdYiFHHq0LFT3h1I5BlqzY8nMJZ61PgY0CRW9bsREl1OnJgFmDszFMmoyTrQ1B9xFJWn_g1AGYa_gQU7fN_GmX3IyifhsADWFYq&returnUrl=https://www.xycq.gov.cn/html/query/agree/list.html?navPage=1')

        time.sleep(1)
        # html = self.driver.page_source
        # if re.search(r'点击任意处继续访问', html):
        #     self.driver.find_element_by_class_name("xycq123").click()
        #     time.sleep(2)
        # # 切换进iframe内
        # iframe = self.driver.find_element_by_tag_name('iframe')
        # self.driver.switch_to_frame(iframe)


    def get_sign(self):
        while True:
            time.sleep(2)
            html = self.driver.page_source
            # slider_base64 img_base64
            img_base64 = re.findall(r'image/png;base64,([\s\S]*?)&quot;\) \d+px', html)
            slider_base64 = re.findall(r'image/png;base64,([\s\S]*?)&quot;', html)
            if not slider_base64:
                continue

            slider_img = Image.open(BytesIO(base64.b64decode(slider_base64[0].encode())))
            image = Image.open(BytesIO(base64.b64decode(img_base64[-1].encode())))

            positions = re.findall(r'\) (\d+)px (\d+)px;', html)
            normal_img = Image.new("RGBA", (260, 118))
            for index, pixeles in enumerate(positions):
                x, y = [int(i) for i in pixeles]
                x1 = abs(x - 260)
                x2 = abs(x1 + 20)
                y1 = abs(y - 118)
                y2 = y1 + 59
                im = image.crop(box=(x1, y1, x2, y2))
                normal_img.paste(im, box=(index * 20 if index < 13 else (index - 13) * 20, 0 if index < 13 else 59))
            normal_img = self.handler(normal_img)
            slider_img = self.handler(slider_img)
            x, y = self.compare(normal_img, slider_img)
            x_tracks = self.get_track(x + 20 + 10 + 62) # 因为这个是背景图外，要加加上此图的宽度
            y_tracks = self.get_track(y + 12)
            tracks = self.get_tracks(x_tracks, y_tracks)
            self.dragging(tracks)


            time.sleep(2)
            html = self.driver.page_source
            if re.search(r'行政许可与行政处罚双公示', html):
                print(self.driver.get_cookies())

    def dragging(self, tracks):
        button = self.driver.find_element_by_xpath('//div[@id]')
        ActionChains(self.driver).click_and_hold(button).perform()

        for x, y in tracks:
            # ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=random.randint(0,2)).perform()
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=y).perform()


        time.sleep(0.18)

        ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()

        time.sleep(0.7)
        ActionChains(self.driver).release().perform()

    @staticmethod
    def get_tracks(x_tracks, y_tracks):
        x_length = len(x_tracks)
        y_length = len(y_tracks)
        if x_length > y_length:
            y_tracks.extend([0 for i in range(x_length - y_length)])
        elif x_length < y_length:
            x_tracks.extend([0 for i in range(y_length - x_length)])
        tracks = []
        for i in range(len(x_tracks)):
            tracks.append((x_tracks[i], y_tracks[i]))
        return tracks

    @staticmethod
    def compare(background, silder):
        """
        background: 宽260 高118
        silder:  宽62 高53

        """
        # background.show()
        # silder.show()
        silder_array = np.array(silder)
        background_array = np.array(background)
        min_value = 999999
        height, width = silder_array.shape
        x_value, y_value, pix_array = 0, 0, np.array([])
        for x in range(31, 229):
            for y in range(25, 93):
                pix = background_array[y:y + height, x:x + width]
                if pix.shape == (height, width):
                    value = abs(np.sum(np.abs(silder_array - pix)))
                    if value < min_value:
                        min_value = value
                        x_value = x
                        y_value = y
                        pix_array = pix
        new_img = Image.new("RGBA", (200, 100))
        aim = Image.fromarray(pix_array)
        new_img.paste(silder, box=(0, 0))
        new_img.paste(aim, box=(100, 0))
        # new_img.show()
        return x_value, y_value

    @staticmethod
    def handler(image):
        if isinstance(image, str):
            img = Image.open(image).convert("L")  # 读图片并转化为灰度图
        else:
            img = image.convert("L")
        img_array = np.array(img)  # 转化为数组
        w, h = img_array.shape
        img_border = np.zeros((w - 1, h - 1))
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                Sx = img_array[x + 1][y - 1] + 2 * img_array[x + 1][y] + img_array[x + 1][y + 1] - \
                     img_array[x - 1][y - 1] - 2 * \
                     img_array[x - 1][y] - img_array[x - 1][y + 1]
                Sy = img_array[x - 1][y + 1] + 2 * img_array[x][y + 1] + img_array[x + 1][y + 1] - \
                     img_array[x - 1][y - 1] - 2 * \
                     img_array[x][y - 1] - img_array[x + 1][y - 1]
                img_border[x][y] = (Sx * Sx + Sy * Sy) ** 0.5
        img2 = Image.fromarray(img_border)
        return img2



    def get_track(self, distance):
        """
        根据偏移量和手动操作模拟计算移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0
        while current < distance:
            if current < mid:
                a = random.uniform(2, 5)
            else:
                a = -(random.uniform(12.5, 13.5))
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t * t
            current += x

            if 0.6 < current - distance < 1:
                x = x - 0.53
                tracks.append(round(x, 2))

            elif 1 < current - distance < 1.5:
                x = x - 1.4
                tracks.append(round(x, 2))
            elif 1.5 < current - distance < 3:
                x = x - 1.8
                tracks.append(round(x, 2))
            else:
                tracks.append(round(x, 2))
        return tracks


if __name__ == '__main__':
    toutiao = Toutiao()
    toutiao.get_sign()
#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: parse_ttf
@time: 2020/11/27
@email: coderflying@163.com
@desc: 
"""
import os
import json
import base64
import logging
import warnings
from io import BytesIO

from reportlab.graphics.shapes import Path
from reportlab.lib import colors
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing
from PIL import Image
from math import ceil
from fontTools.ttLib import TTFont

from .baidu_ocr import Baidu
from .util import ReportLabPen
from .settings import *


class ParseTTFFont:

    baidu = Baidu(access_token=ACCESS_TOKEN)

    def __init__(self, font, ignore_names=[], overwrite_ignore=False):
        if isinstance(font, str):
            self.font = TTFont(font)
        elif isinstance(font, bytes):
            self.font = TTFont(BytesIO(font))
        else:
            raise ValueError('unknown font type')
        self.glyphnames = self.font.getGlyphOrder()
        self.ignore_names = ignore_names if overwrite_ignore else ignore_names + IGNORE_NAMES

    def parse_fonts(self, project):
        """
        根据ttf所属项目找到其对应的结果集json解析文件，如果是新的project,将会自动生产结果集
        :param project: 文件所属项目
        :return:
        """
        project = project + ".json"
        json_path = os.path.join(os.path.join(os.path.dirname(__file__), "font_jsons"), project)
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                font_json = json.load(f)
        else:
            font_json = self.get_fonts_by_orc()
            logging.info(f"结果json保存路径为:{json_path}")
            # 保存
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(font_json, f)

        fonts_coordinate_matrix = self.get_font_message()

        temp_dict, result = {}, {}
        for item in fonts_coordinate_matrix:
            if not isinstance(temp_dict.get(item.get("endPtsOfContours")), list):
                temp_dict[item.get("endPtsOfContours")] = [item]
            else:
                temp_dict[item.get("endPtsOfContours")].append(item)
        for key, item_list in temp_dict.items():
            if len(item_list) == 1:
                # 可以直接根据endPtsOfContours 进行区分
                result[item_list[0].get("glyphname")] = font_json.get(item_list[0].get("endPtsOfContours"))
            else:
                # 有多个字体拥有相同的endPtsOfContours， 那么使用像素坐标点的平均值排序进行区分字体(可能出现意外情况导致识别错误)
                item_list.sort(key=lambda item: self.avg(item["coordinates"]))
                for index, item in enumerate(item_list):
                    result[item.get("glyphname")] = font_json.get(item.get("endPtsOfContours"))[index]

        cmaps = self.font.getBestCmap()
        fonts_result = {}
        for cmap_id, glyname in cmaps.items():
            fonts_result[hex(cmap_id)] = result.get(glyname)
        return fonts_result

    def get_fonts_by_orc(self):
        """
        根据font文件获取 每个字体ID所对应的文字
        通过字体的contoursOfPts得到已知字体字典，如果contoursOfPts值出现一样的，则对比一个最佳坐标点进行辨认
        所谓最佳坐标点，在这里是取一个坐标差值很大的点。
        :param fonts_coordinate_matrix:
        :return: font_json 返回一个已知的字体json文件
        """
        fonts_coordinate_matrix = self.get_coordinate_matrix_and_value()
        temp_dict, result = {}, {}
        for item in fonts_coordinate_matrix:
            if not isinstance(temp_dict.get(item.get("endPtsOfContours")), list):
                temp_dict[item.get("endPtsOfContours")] = [item]
            else:
                temp_dict[item.get("endPtsOfContours")].append(item)
        for endPtsOfContours, item_list in temp_dict.items():
            if len(item_list) == 1:
                result[endPtsOfContours] = item_list[0].get("value")
            else:
                item_list.sort(key=lambda item: self.avg(item["coordinates"]))
                result[endPtsOfContours] = [item.get("value") for item in item_list]
        return result

    def accurate_basic(self):
        """
        使用百度API接口获取转成图片后的ttf， DEBUG模式下可以补入未识别到的文字
        :return:
        """
        word_list = []
        image, name_list, image_dict = self.ttf_to_image()
        response = self.baidu.accurate_basic_of_pillow(image)
        print(response.json())
        [word_list.extend(list(words.get("words"))) for words in response.json().get("words_result")]
        logging.info(f"百度识图结果:{word_list}")
        words = dict(zip(name_list, word_list))
        if len(word_list) is not len(name_list):
            # 有未识别到的字，数量少可以手动添加，数量大，拜拜
            warnings.warn("words length is not equal to gly length,")
            if DEBGU:
                # 非debug模式，忽略识别失败的字体
                for glyname, faild in self.get_orc_faild_font(words, name_list, image_dict).items():
                    faild.show()
                    word = input("请输入图片中显示的文字:")
                    words[glyname] = word
        return words

    def get_coordinate_matrix_and_value(self):
        """
        百度orc识别文字，生产特征字典
        :return:
        """
        words = self.accurate_basic()
        fonts_coordinate_matrix = []
        for glyphname, word in words.items():
            if glyphname[0] in ['.', 'g'] or glyphname in self.ignore_names:  # 跳过'.notdef', '.null'
                continue
            item = {}
            glyph = self.font['glyf'][glyphname]
            item["coordinates"] = glyph.coordinates._a.tolist()
            item["endPtsOfContours"] = base64.b64encode(str(glyph.endPtsOfContours).encode("utf-8")).decode("utf-8")
            item["value"] = word
            fonts_coordinate_matrix.append(item)
        return fonts_coordinate_matrix

    def get_font_message(self):
        """
        获取字体文件信息
            coordinates: 该字体所有x,y坐标(固定顺序) [x,y,x1,y1,x2,y2...]
            endPtsOfContours: 根据contours和pt对应关系，形成的列表，然后编码为base64作为ID
                              始 endPtsOfContours， 记录contours和pt坐标对应的关系，如[3,9] 代表 该字体有2个contour，
                              第一个contour 包含前四个坐标点[0,1,2,3], 第二个包含[4,5,6,7,8,9]六个点。所有的偶数位为x，奇数位为y
        :return:
        """
        fonts_coordinate_matrix = []  # 结果集
        for glyphname in self.glyphnames:  # 根据name遍历字体文件中的所有字体
            if glyphname[0] in ['.', 'g'] or glyphname in self.ignore_names:  # 跳过'.notdef', '.null' 'x'
                continue
            item = {}
            glyph = self.font['glyf'][glyphname]
            item["coordinates"] = glyph.coordinates._a.tolist()
            item["endPtsOfContours"] = base64.b64encode(str(glyph.endPtsOfContours).encode("utf-8")).decode("utf-8")
            item["glyphname"] = glyphname
            fonts_coordinate_matrix.append(item)
        if DEBGU:
            logging.debug(msg=fonts_coordinate_matrix)
        return fonts_coordinate_matrix

    def ttf_to_image(self):
        """
        将ttf字体文件的字体绘制在Image对象上
        :return:
        """
        glyphset = self.font.getGlyphSet()
        size = (BASE_BACKGOUND_WIDTH * FONT_NUMS_PER_LINE,
                ceil(len(self.glyphnames) / FONT_NUMS_PER_LINE) * BASE_BACKGOUND_HEIGHT)  # 背景图片尺寸
        image = Image.new("RGB", size=size, color=(255, 255, 255))  # 初始化背景图片
        name_list, image_dict = [], {}
        for index, glyphname in enumerate(self.glyphnames):
            if glyphname[0] in ['.', 'g'] or glyphname in self.ignore_names:  # 跳过'.notdef', '.null'
                continue
            g = glyphset[glyphname]
            pen = ReportLabPen(self.glyphnames, Path(fillColor=colors.black, strokeWidth=1))
            g.draw(pen)
            # w, h = g.width, g.width
            w, h = g.width if g.width > 1000 else 1000, g.width if g.width > 1000 else 1000
            g = Group(pen.path)
            g.translate(0, 200)
            d = Drawing(w, h)
            d.add(g)
            im = renderPM.drawToPIL(d, dpi=72).resize((FONT_WIDTH, FONT_HEIGHT))
            box = (
                (index % FONT_NUMS_PER_LINE) * BASE_BACKGOUND_WIDTH,
                (index // FONT_NUMS_PER_LINE) * BASE_BACKGOUND_HEIGHT)
            image.paste(im, box=box)
            name_list.append(glyphname)
            image_dict[glyphname] = im
        return image, name_list, image_dict

    @staticmethod
    def get_orc_faild_font(words, name_list, image_dict):
        faild_fonts_img = {}
        for glypname in name_list:
            if not words.get(glypname):
                faild_fonts_img[glypname] = image_dict.get(glypname)
        return faild_fonts_img

    @staticmethod
    def avg(alist):
        return sum(alist) // len(alist)


if __name__ == '__main__':
    pass

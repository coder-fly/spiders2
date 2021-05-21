"""

"""
import base64
import json
import os
from io import BytesIO
from math import ceil

import pytesseract
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont


class FontParser:
    cache_path = os.path.join(os.path.dirname(__file__), "jsons")

    def __init__(self, font, project, offset=1, ocr_always=False, cache_path=None, sort=False):
        """

        :param font: 字体文件地址或响应的content
        :param project: 所属项目
        :param offset: 偏移量
        :param ocr_always: 是否每次都调用orc解析
        :param cache_path: json文件保存目录
        :param sort: 是否进行排序(排序后的顺序与通过fontcreator一致，便于检查)

        """
        if isinstance(font, str):
            self.font = TTFont(font)
            self._font = font
        elif isinstance(font, bytes):
            self.font = TTFont(BytesIO(font))
            self._font = BytesIO(font)
        else:
            raise ValueError('unknown font type')
        self.project = project
        self.ocr_always = ocr_always
        if cache_path:
            self.cache_path = cache_path
        os.makedirs(self.cache_path, exist_ok=True)
        self.project_json_path = os.path.join(self.cache_path, '{}.json'.format(project))
        self.glyphnames = self.font.getGlyphOrder()[offset:]
        self.sort = sort

    def parse(self):
        if self.ocr_always:
            return self._parse()
        else:
            if os.path.exists(self.project_json_path):
                results = self._compare()
            else:
                results = self._parse()
                self._generate_json(results)
        return results

    def _compare(self):
        temp_dict, result, fonts_coordinate_matrix = {}, {}, []
        with open(self.project_json_path, "r") as f:
            font_json = json.load(f)
        for glyphname in self.glyphnames:  # 根据name遍历字体文件中的所有字体
            item = {}
            glyph = self.font['glyf'][glyphname]
            item["weight"] = sum(glyph.coordinates._a.tolist()) / len(glyph.coordinates._a.tolist())
            item["fid"] = base64.b64encode(str(glyph.endPtsOfContours).encode("utf-8")).decode("utf-8")
            item["glyphname"] = glyphname
            fonts_coordinate_matrix.append(item)
        for item in fonts_coordinate_matrix:
            if not isinstance(temp_dict.get(item.get("fid")), list):
                temp_dict[item.get("fid")] = [item]
            else:
                temp_dict[item.get("fid")].append(item)
        for key, item_list in temp_dict.items():
            if len(item_list) == 1:
                # 可以直接根据endPtsOfContours 进行区分
                result[item_list[0].get("glyphname")] = font_json.get(item_list[0].get("fid"))
            else:
                # 有多个字体拥有相同的endPtsOfContours， 那么使用像素坐标点的平均值排序进行区分字体(可能出现意外情况导致识别错误)
                item_list.sort(key=lambda item: item['weight'])
                for index, item in enumerate(item_list):
                    result[item.get("glyphname")] = font_json.get(item.get("fid"))[index]
        # sort
        if self.sort:
            result = {key:value for key, value in sorted(result.items(), key=lambda kv:self.glyphnames.index(kv[0]))}
        return result
    def _generate_json(self, results: dict):
        """生成特征文件"""
        temp, result = {}, {}
        for glyphname, value in results.items():
            item = {}
            glyph = self.font['glyf'][glyphname]
            coordinates = glyph.coordinates._a.tolist()
            fid = base64.b64encode(str(glyph.endPtsOfContours).encode("utf-8")).decode("utf-8")
            item['fid'] = fid
            item['weight'] = sum(coordinates) / len(coordinates)
            item['value'] = value
            # 已经存在相同id的数据
            if isinstance(temp.get(fid), list):
                temp[fid].append(item)
            else:
                temp[fid] = [item]
        for fid, item_list in temp.items():
            if len(item_list) == 1:
                result[fid] = item_list[0].get("value")
            else:
                item_list.sort(key=lambda item: item['weight'])
                result[fid] = [item.get("value") for item in item_list]
        with open(self.project_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f)

    def _parse(self):

        lines = ceil(len(self.glyphnames) / 40)
        array_list = np.array_split(self.glyphnames, lines)
        im = Image.new("RGB", (1800, (lines + 1) * 50), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(self._font, 40)
        for line in range(lines):
            alist = [i.replace("uni", "\\u") for i in array_list[line]]
            text = "".join(alist)
            text = text.encode('utf-8').decode('unicode_escape')
            draw.text((0, 50 * line), text, font=font, fill="#000000")
        result = pytesseract.image_to_string(im, lang="chi_sim")
        result = result.replace(" ", "").replace("\n", "")
        return dict(zip(self.glyphnames, list(result)))

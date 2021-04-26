#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: tools
@time: 2021/4/1
@email: coderflying@163.com
@desc: 
"""

from io import BytesIO

import numpy as np
from PIL import Image, ImageFilter


class ImageHandler():

    def __init__(self, path):
        if isinstance(path, str):
            self.image = Image.open(path)
        else:
            self.image = Image.open(BytesIO(path))

    def remove_noise(self):
        """
        移除噪点，该样例中噪点的像素值为0，0，0
        :return:
        """
        img_array = np.array(self.image)
        shape = img_array.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                value = img_array[i, j]
                if not any(value):  # 如果value == [0,0,0]
                    img_array[i, j] = [255, 255, 255]
        self.image = Image.fromarray(img_array)

    def remove_background(self):
        """
        去除背景图，
        :return:
        """
        img_array = np.array(self.image)
        color, counts = np.unique(img_array.reshape(-1, 3), axis=0, return_counts=True)
        color_list = [color[index] for index, count in enumerate(counts, 0) if 500 <= count <= 2200]

        mask = np.zeros(img_array.shape, np.uint8) + 255  # 生成一个全是白色的图片

        for color in color_list:
            mask[np.all(img_array == color, axis=-1)] = img_array[np.all(img_array == color, axis=-1)]
        self.image = Image.fromarray(mask)

    def remove_noise_line(self):
        """
        去除干扰线, 本例中文字均匀分布在3x3的方格里，而干扰线穿插与两个之间的位置，遍历两个之间的位置，如果不是白色，则这个颜色就是干扰线

        大概位置  x轴    y轴
                0-20   0-300
                100-120 0-300
                200-220 0-300
                0-300  0-10
                0-300  100-110
                0-300  200-210
        :return:
        """
        img_array = np.array(self.image)
        shape = img_array.shape
        color_list = []
        for j in range(shape[0]):
            for i in range(shape[1]):
                value = img_array[i, j]
                if j <= 20 or 110 <= j <= 120:
                    if value.tolist() != [255, 255, 255]:
                        color_list.append(value)
                elif i <= 10 or 100 <= i <= 110 or 200 <= i <= 210:
                    if value.tolist() != [255, 255, 255]:
                        color_list.append(value)
        color_list = np.unique(color_list, axis=0)
        for color in color_list:
            img_array[np.all(img_array == color, axis=-1)] = [255, 255, 255]
        self.image = Image.fromarray(img_array)

    def grayscale_corrosion(self):
        """
        灰度处理并腐蚀
        :return:
        """
        img_array = np.array(self.image)
        img_array[np.all(img_array != np.array([255, 255, 255]), axis=-1)] = [0, 0, 0] # 灰度处理
        self.image = Image.fromarray(img_array)
        self.image = self.image.filter(ImageFilter.MinFilter(3)) # 腐蚀

    def cut(self):
        img_array = np.array(self.image)
        shape = img_array.shape
        for j in range(1,3):
            for i in range(3):
                cut_array = img_array[i * 100:(i +1)*100,j*(100):(j+1)*100]
                print(cut_array.var())
                # Image.fromarray(cut_array).show()
            return
    def run_test(self):
        self.remove_noise()  # 去除噪点
        self.remove_background()  # 去除背景
        self.remove_noise_line()  # 去除干扰线并灰度
        self.grayscale_corrosion()  # 灰度处理并腐蚀
        # self.cut()  # 灰度处理并腐蚀
        # self.image.show()
        # self.image.save('temp.png')
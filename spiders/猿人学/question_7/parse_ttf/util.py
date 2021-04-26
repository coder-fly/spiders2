#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: util
@time: 2020/12/4
@email: coderflying@163.com
@desc: 
"""
from __future__ import print_function, division, absolute_import
from fontTools.pens.basePen import BasePen
from reportlab.graphics.shapes import Path


class ReportLabPen(BasePen):
    """A pen for drawing onto a reportlab.graphics.shapes.Path object."""

    def __init__(self, glyphSet, path=None):
        BasePen.__init__(self, glyphSet)
        if path is None:
            path = Path()
        self.path = path

    def _moveTo(self, p):
        (x, y) = p
        self.path.moveTo(x, y)

    def _lineTo(self, p):
        (x, y) = p
        self.path.lineTo(x, y)

    def _curveToOne(self, p1, p2, p3):
        (x1, y1) = p1
        (x2, y2) = p2
        (x3, y3) = p3
        self.path.curveTo(x1, y1, x2, y2, x3, y3)

    def _closePath(self):
        self.path.closePath()
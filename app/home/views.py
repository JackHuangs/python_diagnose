#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 19:09
# @Author  : huangs
# @Email   : 826652961@qq.com
# @File    : views.py
# @Software: PyCharm
from . import home


@home.route("/")
def index():
    return "this is home view"


@home.route('/test')
def test():
    return "this is test view"

#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 20:46
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : views.py
# @Software: PyCharm
from .import admin
import os


@admin.route("/")
def index():
    """首页

    @@@
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    return "this is admin view !"

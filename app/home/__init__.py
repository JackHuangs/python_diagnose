#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 19:04
# @Author  : huangs
# @Email   : 826652961@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

home = Blueprint("home", __name__)

import app.home.views
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 18:58
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : server.py
# @Software: PyCharm
from app import app

application = app

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True)

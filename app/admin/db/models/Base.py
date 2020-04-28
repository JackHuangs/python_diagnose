#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/26 11:37
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : Base.py
# @Software: PyCharm
from app.admin.db.manager import db


if __name__ == '__main__':
    db.create_all()


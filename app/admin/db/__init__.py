#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 16:59
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy
from app import app

# set the mysql environment
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@182.61.24.246:3306/diagnose"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# init mysql
db = SQLAlchemy(app)

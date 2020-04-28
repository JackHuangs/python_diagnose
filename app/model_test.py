#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 12:01
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : model_test.py
# @Software: PyCharm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# set the mysql environment
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = "3306"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@127.0.0.1:3306/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


# 权限
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    adminlogs = db.relationship('Adminlog', backref="admin", cascade='all, delete-orphan')


# 会员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))


if __name__ == '__main__':
    db.create_all()

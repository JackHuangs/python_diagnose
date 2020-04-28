#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/26 11:33
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : UserLog.py
# @Software: PyCharm
from app.admin.db.manager import db
from datetime import datetime


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))  # 最近登录IP地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间
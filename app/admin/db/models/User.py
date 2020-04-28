#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/26 11:29
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : User.py
# @Software: PyCharm
from app.admin.db.manager import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 会员模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(11))
    info = db.Column(db.Text)
    token = db.Column(db.String(255), unique=True)
    wechat_avatar = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)
    userlogs = db.relationship('Userlog', backref="user")  # 会员日志外键关系

    def hash_password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.pwd, pwd)

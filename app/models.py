#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 19:03
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : models.py
# @Software: PyCharm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.admin.db import db


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
    openid = db.Column(db.String(255), unique=True)
    userlogs = db.relationship('Userlog', backref="user")  # 会员日志外键关系
    userptos = db.relationship('Userpto', backref="user")

    def hash_password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.pwd, pwd)


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


# 诊断图片
class Userpto(db.Model):
    __tablename__ = 'userpto'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_pto_url = db.Column(db.String(255))
    face_pto_url = db.Column(db.String(255))
    left_eye_pto_url = db.Column(db.String(255))
    right_eye_pto_url = db.Column(db.String(255))
    nose_pto_url = db.Column(db.String(255))
    mouth_pto_url = db.Column(db.String(255))
    tongue_pto_url = db.Column(db.String(255))
    is_valid = db.Column(db.Integer)
    result = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    code = db.Column(db.String(255), unique=True)
    level = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    info = db.Column(db.String(100))
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship('Admin', backref="role")


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    token = db.Column(db.String(255), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('Adminlog', backref="admin")
    oplogs = db.relationship('Oplog', backref="admin")

    def hash_password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员编号
    ip = db.Column(db.String(100))  # 最近登录IP地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员编号
    ip = db.Column(db.String(100))  # 最近登录IP地址
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(100))
    menu_path = db.Column(db.String(100))
    menu_icon = db.Column(db.String(100))
    parent_id = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


class Disease(db.Model):
    __tablename__ = "disease"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_index = db.Column(db.Integer)
    photo = db.Column(db.String(100))
    desc = db.Column(db.Text)
    cate_id = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    
class Banner(db.Model):
    __tablename__ = "banner"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(100))
    desc = db.Column(db.Text)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


class Cate(db.Model):
    __tablename__ = "cate"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    icon = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    is_index = db.Column(db.SmallInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

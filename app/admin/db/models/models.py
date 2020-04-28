#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 19:03
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : models.py
# @Software: PyCharm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.admin.db.manager import db


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
    comments = db.relationship('Comment', backref="user")
    moviecols = db.relationship('Moviecol', backref="user")

    def __repr__(self):
        return "<User %r>" % self.name

    def hash_password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.pwd, pwd)


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员编号
    ip = db.Column(db.String(100))  # 最近登录IP地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 图片管理
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

    def __repr__(self):
        return "<Userpto %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    movies = db.relationship("Movie", backref="tag")

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('Comment', backref="movie")
    moviecols = db.relationship('Moviecol', backref="movie")

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtiem = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Moviecol %r>' % self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Role %r>" % self.name


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

    def __repr__(self):
        return "<Admin %r>" % self.name

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
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员编号
    ip = db.Column(db.String(100))  # 最近登录IP地址
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == "__main__":
    db.create_all()

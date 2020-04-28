#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 17:41
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : Auth.py
# @Software: PyCharm
from flask import request, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app import app
from app.models import User, Role, Admin, Auth
from functools import wraps


def generate_auth_token(user_id, expiration=36000):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user_id}).decode("ascii")
    return token


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    user = User.query.get(data['id'])
    return user


def login_required(view_func):
    @wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(status=4103, msg='缺少参数token')

        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
            global token_id
            token_id = data['id']
        except SignatureExpired:
            return jsonify(status=4101, msg="登录已过期,请重新登录")
        except BadSignature:
            return jsonify(status=4102, msg="token is invalid")

        return view_func(*args, **kwargs)

    return verify_token


def permission_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.endpoint.split('.')
        endpoint = auth[1]
        res = Admin.query.join(Role).filter(Role.id == Admin.role_id, Admin.id == token_id).first()
        auths = res.role.auths
        auths = list(map(lambda v: int(v), auths.split(",")))
        res = Auth.query.filter_by(code=endpoint).first()
        if not(res.id in auths):
            return jsonify({"status": 403, "msg": "你没有权限,请联系超级管理员"})
        return f(*args, **kwargs)
    return decorated


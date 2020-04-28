#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:17
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : admin_login.py
# @Software: PyCharm
from . import admin
from flask import request, jsonify
from app.models import Admin, Adminlog
from app.admin.db import db
from app.admin.common.Auth import generate_auth_token


@admin.route('/admin/login', methods=["POST"])
def admin_login():
    """管理员登录

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    username    |    false    |    string   |    用户名    |
    |    password    |    false    |    string   |    密码    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200, "token": "token"}
    @@@
    """
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return jsonify({
            "status": 400,
            "msg": "用户名或密码不能为空"
        })
    res = Admin.query.filter_by(name=username).first()
    if not res:
        return jsonify({"status": 201, "msg": "未找到该管理员"})
    if res.verify_password(password):
        admin_id = res.id
        ip = request.remote_addr
        token = generate_auth_token(res.id)
        log = Adminlog(admin_id=admin_id, ip=ip)
        res.token = token
        db.session.add(log)
        db.session.commit()
        return jsonify({"status": 200, "token": token, "msg": "登录成功", "admin_id": res.id})
    else:
        return jsonify({"status": 202, "msg": "密码错误"})

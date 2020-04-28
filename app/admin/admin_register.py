#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:31
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : admin_register.py
# @Software: PyCharm
from . import admin
from flask import request, jsonify
from app.models import Admin
from app.admin.db import db
from app.admin.common.Auth import login_required, permission_required


@admin.route("/admin/register", methods=["POST"])
@login_required  # 必须登录的装饰器校验
@permission_required
def admin_register():
    """注册管理员

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    name    |    false    |    String   |    用户名    |
    |    pwd    |    false    |    String   |    密码    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    username = request.form.get('name')
    password = request.form.get('pwd')
    if username is None or password is None:
        return jsonify({
            "status": 201,
            "msg": "用户名或密码不能为空"
        })
    if Admin.query.filter_by(name=username).first() is not None:
        return jsonify({
            "status": 400,
            "msg": "管理员已存在"
        })
    res = Admin(name=username)
    res.hash_password(password)
    db.session.add(res)
    db.session.commit()
    return jsonify({
        "username": res.name,
        "status": 200,
        "msg": "注册成功"
    })

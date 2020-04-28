#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 12:27
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : admin_pwd_edit.py
# @Software: PyCharm
from . import admin
from app.models import Admin
from app.admin.common.Auth import login_required
from flask import request, jsonify
from app.admin.db import db


@admin.route('/admin/pwd/edit/<int:admin_id>', methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
def admin_pwd_edit(admin_id):
    """管理员修改个人密码

        @@@
        #### args

        | args | nullable | type | remark |
        |--------|--------|--------|--------|
        |    admin_id    |    False    |    Int   |    管理员ID    |
        |    pwd    |    True    |    String   |    密码    |

        #### return
        - ##### json
        > {"msg": "success", "code": 200}
        @@@
        """
    admin_id = admin_id
    res = Admin.query.filter_by(id=admin_id).first()
    res.hash_password(request.form.get('pwd')) if request.form.get('pwd') else res.pwd
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})

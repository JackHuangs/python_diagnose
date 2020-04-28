#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:47
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : user_profile_edit.py
# @Software: PyCharm
from . import admin
from flask import request, jsonify
from app.models import User
from app.admin.db import db
from app.admin.common.Auth import login_required


@admin.route('/user/edit/<int:user_id>', methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
def user_profile_edit(user_id):
    """编辑用户信息

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    user_id    |    False    |    Int   |    用户ID    |
    |    name    |    True    |    String   |    用户昵称    |
    |    email    |    True    |    String   |    邮件    |
    |    phone    |    True    |    String   |    手机号码    |
    |    wechat_avatar    |    True    |    String   |    微信头像    |
    |    info    |    True    |    String   |    个人信息    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    user_id = user_id
    res = User.query.filter_by(id=user_id).first()
    name = request.form.get('name') if request.form.get('name') else res.name
    res.hash_password(request.form.get('pwd')) if request.form.get('pwd') else res.pwd
    email = request.form.get('email') if request.form.get('email') else res.email
    phone = request.form.get('phone') if request.form.get('phone') else res.phone
    info = request.form.get('info') if request.form.get('info') is not None else res.info
    wechat_avatar = request.form.get('wechat_avatar') if request.form.get('wechat_avatar') else res.wechat_avatar
    res.name = name
    res.email = email
    res.phone = phone
    res.info = info
    res.wechat_avatar = wechat_avatar
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})

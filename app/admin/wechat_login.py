#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:39
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : wechat_login.py
# @Software: PyCharm
from . import admin
from flask import request, jsonify
from app.models import User, Userlog
from app.admin.db import db
from app.admin.common.Wechat_code import get_code
from app.admin.common.Auth import generate_auth_token


@admin.route('/wechat/login', methods=["GET"])
def wechat_login():
    """微信用户自动注册和登录

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    code    |    false    |    String   |    小程序wx.login后的code    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    code = request.args.get('code')
    openid = get_code(code)
    res = User.query.filter_by(openid=openid).first()
    ip = request.remote_addr
    token = generate_auth_token(code)
    if not res:
        res = User(openid=openid, token=token)
        db.session.add(res)
        db.session.commit()
        user = User.query.filter_by(openid=openid).first()
        logs = Userlog(user_id=user.id, ip=ip)
        db.session.add(logs)
        db.session.commit()
        return jsonify({"status": 200, "msg": "登录成功", "token": token, "user_id": user.id})
    else:
        logs = Userlog(user_id=res.id, ip=ip)
        res.token = token
        db.session.add(logs)
        db.session.commit()
        return jsonify({"status": 200, "msg": "已经登录了", "token": res.token, "user_id": res.id})

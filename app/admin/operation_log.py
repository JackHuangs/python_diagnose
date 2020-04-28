#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 13:59
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : operation_log.py
# @Software: PyCharm
from . import admin
from app.models import Userlog, Adminlog
from app.admin.common.utils import dict_to_json
from app.admin.common.Auth import login_required, permission_required
from flask import request


@admin.route("/user/log", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def get_user_log():
    """获取用户登录日志

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    page    |    True    |    Int   |    当前页数    |
    |    pagesize    |    True    |    Int   |    每一页的数量    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    page = int(request.args.get("page")) if request.args.get("page") else 1
    per_page = int(request.args.get("pagesize")) if request.args.get("pagesize") else 10
    total = Userlog.query.count()
    res = Userlog.query.order_by(Userlog.addtime.desc()).paginate(page=page, per_page=per_page)
    res = res.items
    return dict_to_json(res, total)


@admin.route("/admin/log", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def get_admin_log():
    """获取管理员登录日志

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    page    |    True    |    Int   |    当前页数    |
    |    pagesize    |    True    |    Int   |    每一页的数量    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    page = int(request.args.get("page")) if request.args.get("page") else 1
    per_page = int(request.args.get("pagesize")) if request.args.get("pagesize") else 10
    total = Adminlog.query.count()
    res = Adminlog.query.order_by(Adminlog.addtime.desc()).paginate(page=page, per_page=per_page)
    res = res.items
    return dict_to_json(res, total)

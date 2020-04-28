#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:43
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : user_profile_list.py
# @Software: PyCharm
from . import admin
from app.models import User
from app.admin.common.Auth import login_required
from app.admin.common.utils import dict_to_json
from flask import request


@admin.route('/user/list', methods=["GET"])
@login_required  # 必须登录的装饰器校验
def user_profile_list():
    """查询用户信息

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    user_id    |    True    |    String   |    用户ID    |
    |    page    |    True    |    Int   |    当前页数    |
    |    pagesize    |    True    |    Int   |    每一页的数量    |
    |    keyword    |    True    |    String   |    关键词    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    page = int(request.args.get("page")) if request.args.get("page") else 1
    key_word = request.args.get("keyword") if request.args.get("keyword") else ""
    per_page = int(request.args.get("pagesize")) if request.args.get("pagesize") else 10
    user_id = int(request.args.get("user_id")) if request.args.get("user_id") else ""
    if user_id:
        res = User.query.filter_by(id=user_id).all()
        total = 1
    else:
        total = User.query.count()
        if key_word:
            res = User.query.filter(User.name.ilike('%'+key_word+"%")).order_by(User.addtime.desc()).paginate(page=page, per_page=per_page)
            total = User.query.filter(User.name.ilike('%'+key_word+"%")).count()
        else:
            res = User.query.order_by(User.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


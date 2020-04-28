#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:51
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : user_diagnosis_pto.py
# @Software: PyCharm
from . import admin
from app.models import Userpto
from app.admin.common.utils import dict_to_json
from app.admin.common.Auth import login_required
from flask import request, jsonify
from app.admin.db import db


@admin.route('user/diagnosis', methods=["GET"])
@login_required  # 必须登录的装饰器校验
def user_diagnosis_pto():
    """获取用户诊断图片列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    user_id    |    True    |    Int   |    用户ID    |
    |    page    |    True    |    Int   |    当前页数    |
    |    pagesize    |    True    |    Int   |    每一页的数量    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    page = int(request.args.get("page")) if request.args.get("page") else 1
    per_page = int(request.args.get("pagesize")) if request.args.get("pagesize") else 10
    user_id = int(request.args.get("user_id")) if request.args.get("user_id") else ""
    photo_id = int(request.args.get("photo_id")) if request.args.get("photo_id") else ""
    if user_id:
        res = Userpto.query.filter_by(user_id=user_id).all()
        total = Userpto.query.filter_by(user_id=user_id).count()
    elif photo_id:
        res = Userpto.query.filter_by(id=photo_id).all()
        total = 1
    else:
        total = Userpto.query.count()
        res = Userpto.query.paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route('user/diagnosis/<int:photo_id>', methods=["PUT"])
@login_required
def user_photo_diagnose(photo_id):
    photo_id = photo_id
    res = Userpto.query.filter_by(id=photo_id).first()
    result = request.form.get('result') if request.form.get('result') is not None else res.result
    res.result = result
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})

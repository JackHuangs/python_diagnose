#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 19:03
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : super_admin_auth.py
# @Software: PyCharm
from . import admin
from flask import request, jsonify
from app.models import Auth
from app.admin.db import db
from app.admin.common.Auth import login_required, permission_required
from app.admin.common.utils import dict_to_json


@admin.route('admin/auth/add', methods=["POST"])
@login_required  # 必须登录的装饰器校验
@permission_required
def admin_auth_add():
    """添加权限

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    auth_name    |    False    |    String   |    权限昵称    |
    |    auth_code    |    False    |    String   |    权限视图    |
    |    parent_id    |    False    |    Int   |    所属父类权限    |
    |    level        |    True    |    Int   |    权限等级    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    auth_name = request.form.get("auth_name")
    auth_code = request.form.get("auth_code")
    parent_id = request.form.get("parent_id") if request.form.get("parent_id") else 0
    level = request.form.get("level") if request.form.get("level") else 1
    if auth_name is None or auth_code is None:
        return jsonify({
            "status": 201,
            "msg": "权限名或符码不能为空"
        })
    elif Auth.query.filter_by(name=auth_name).first() is not None:
        return jsonify({
            "status": 202,
            "msg": "权限已存在"
        })
    else:
        res = Auth(name=auth_name, code=auth_code, parent_id=parent_id, level=level)
        db.session.add(res)
        db.session.commit()
        return jsonify({
            "username": res.name,
            "status": 200,
            "msg": "添加权限成功"
        })


@admin.route("admin/auth/list", methods=["GET"])
@login_required  # 必须登录的装饰器校验
@permission_required
def admin_auth_list():
    """获取权限列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    auth_id    |    True    |    Int   |    权限ID    |
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
    auth_id = int(request.args.get("auth_id")) if request.args.get("auth_id") else ""
    if auth_id:
        res = Auth.query.filter_by(id=auth_id).all()
        total = 1
    else:
        total = Auth.query.count()
        if key_word:
            res = Auth.query.filter(Auth.name.ilike('%' + key_word + "%")).order_by(Auth.addtime.desc()).paginate(
                page=page, per_page=per_page)
            total = Auth.query.filter(Auth.name.ilike('%' + key_word + "%")).count()
        else:
            res = Auth.query.order_by(Auth.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route("admin/auth/all", methods=["GET"])
@login_required  # 必须登录的装饰器校验
@permission_required
def admin_auth_all():
    """获取全部权限（不分页）

    @@@
    #### args

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    total = Auth.query.count()
    res = Auth.query.all()
    return dict_to_json(res, total)


@admin.route('admin/auth/edit/<int:auth_id>', methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
@permission_required
def auth_edit(auth_id):
    """编辑权限

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    auth_id    |    False    |    Int   |    权限ID    |
    |    auth_name    |    True    |    String   |    权限昵称    |
    |    auth_code    |    True    |    String   |    权限视图    |
    |    parent_id    |    True    |    Int   |    所属父类权限    |
    |    level        |    True    |    Int   |    权限等级    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    auth_id = auth_id
    res = Auth.query.filter_by(id=auth_id).first()
    auth_name = request.form.get('auth_name') if request.form.get('auth_name') else res.auth_name
    auth_code = request.form.get('auth_code') if request.form.get('auth_code') else res.auth_code
    level = request.form.get('level') if request.form.get('level') else res.level
    parent_id = request.form.get('parent_id') if request.form.get('parent_id') else res.parent_id
    res.name = auth_name
    res.code = auth_code
    res.level = level
    res.parent_id = parent_id
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})


@admin.route('admin/auth/del/<int:auth_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
@permission_required
def auth_del(auth_id):
    """删除权限

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    auth_id    |    False    |    Int   |    权限ID    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    auth_id = auth_id
    res = Auth.query.filter_by(id=auth_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

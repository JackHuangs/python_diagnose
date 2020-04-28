#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 19:52
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : role_auth.py
# @Software: PyCharm
from . import admin
from flask import request, jsonify
from app.admin.db import db
from app.models import Role
from app.admin.common.utils import dict_to_json
from app.admin.common.Auth import login_required, permission_required


@admin.route("role/auth/add", methods=["POST"])
@login_required  # 必须登录的装饰器校验
@permission_required
def role_auth_add():
    """添加角色

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    name    |    False    |    String   |    角色昵称    |
    |    auths    |    False    |    String   |    拥有权限    |
    |    info    |    True    |    String   |    角色简介    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    name = request.form.get("name")
    auths = request.form.get("auths")
    info = request.form.get("info") if request.form.get("info") else None
    if name is None:
        return jsonify({
            "status": 201,
            "msg": "角色名"
        })
    elif Role.query.filter_by(name=name).first() is not None:
        return jsonify({
            "status": 202,
            "msg": "角色已存在"
        })
    else:
        res = Role(name=name, auths=auths, info=info)
        db.session.add(res)
        db.session.commit()
        return jsonify({
            "username": res.name,
            "status": 200,
            "msg": "添加角色成功"
        })


@admin.route("role/auth/list", methods=["GET"])
@login_required  # 必须登录的装饰器校验
@permission_required
def role_list():
    """获取角色列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    role_id    |    True    |    Int   |    角色ID    |
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
    role_id = int(request.args.get("role_id")) if request.args.get("role_id") else ""
    if role_id:
        res = Role.query.filter_by(id=role_id).all()
        total = 1
    else:
        total = Role.query.count()
        if key_word:
            res = Role.query.filter(Role.name.ilike('%' + key_word + "%")).order_by(Role.addtime.desc()).paginate(
                page=page, per_page=per_page)
            total = Role.query.filter(Role.name.ilike('%' + key_word + "%")).count()
        else:
            res = Role.query.order_by(Role.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route('role/auth/edit/<int:role_id>', methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
@permission_required
def role_edit(role_id):
    """编辑角色

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    role_id    |    False    |    Int   |    角色ID    |
    |    name    |    True    |    String   |    角色昵称    |
    |    auths    |    True    |    String   |    拥有权限    |
    |    info    |    True    |    String   |    角色简介    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    role_id = role_id
    res = Role.query.filter_by(id=role_id).first()
    name = request.form.get('name') if request.form.get('name') else res.name
    auths = request.form.get('auths') if request.form.get('auths') else res.auths
    info = request.form.get('info') if request.form.get('info') else res.info
    res.name = name
    res.auths = auths
    res.info = info
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})


@admin.route("role/auth/all", methods=["GET"])
@login_required  # 必须登录的装饰器校验
@permission_required
def role_auth_all():
    """获取全部角色（不分页）

    @@@
    #### args

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    total = Role.query.count()
    res = Role.query.all()
    return dict_to_json(res, total)


@admin.route('role/auth/del/<int:role_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
@permission_required
def role_del(role_id):
    """删除角色

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    role_id    |    False    |    Int   |    角色ID    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    role_id = role_id
    res = Role.query.filter_by(id=role_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 12:31
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : menu_list.py
# @Software: PyCharm
from . import admin
from flask import request, jsonify
from app.models import Menu
from app.admin.db import db
from app.admin.common.utils import dict_to_json
from app.admin.common.Auth import login_required, permission_required


@admin.route('menu/add', methods=["POST"])
@login_required
@permission_required
def menu_add():
    """添加菜单

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    menu_name    |    False    |    String   |    菜单昵称    |
    |    menu_path    |    True    |    String   |    菜单路径     |
    |    menu_icon    |    True    |    String   |    菜单图标类    |
    |    parent_id    |    True    |    Int   |    所属菜单    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    menu_name = request.form.get("menu_name")
    menu_path = request.form.get("menu_path") if request.form.get("menu_path") else None
    menu_icon = request.form.get("menu_icon") if request.form.get("menu_icon") else "icon"
    parent_id = request.form.get("parent_id") if request.form.get("parent_id") else 0
    if menu_name is None:
        return jsonify({
            "status": 201,
            "msg": "菜单昵称不能为空"
        })
    elif Menu.query.filter_by(menu_name=menu_name).first() is not None:
        return jsonify({
            "status": 202,
            "msg": "菜单项已存在"
        })
    else:
        res = Menu(menu_name=menu_name, menu_path=menu_path, menu_icon=menu_icon, parent_id=parent_id)
        db.session.add(res)
        db.session.commit()
        return jsonify({
            "username": res.menu_name,
            "status": 200,
            "msg": "添加成功"
        })


@admin.route("menu/edit/<int:menu_id>", methods=["PUT", "PATCH"])
@login_required
@permission_required
def menu_edit(menu_id):
    """编辑菜单

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    menu_id    |    False    |    Int   |    菜单ID    |
    |    menu_name    |    False    |    String   |    菜单昵称    |
    |    menu_path    |    True    |    String   |    菜单路径     |
    |    menu_icon    |    True    |    String   |    菜单图标类    |
    |    parent_id    |    True    |    Int   |    所属菜单    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    menu_id = menu_id
    res = Menu.query.filter_by(id=menu_id).first()
    menu_name = request.form.get("menu_name") if request.form.get("menu_name") else res.menu_name
    menu_path = request.form.get("menu_path") if request.form.get("menu_path") else res.menu_path
    menu_icon = request.form.get("menu_icon") if request.form.get("menu_icon") else res.menu_icon
    parent_id = request.form.get("parent_id") if request.form.get("parent_id") else res.parent_id
    res.menu_name = menu_name
    res.menu_path = menu_path
    res.menu_icon = menu_icon
    res.parent_id = parent_id
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})


@admin.route("menu/all", methods=["GET"])
@login_required
def menu_all():
    """获取全部菜单（不分页）

    @@@
    #### args

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    total = Menu.query.count()
    res = Menu.query.all()
    return dict_to_json(res, total)


@admin.route("menu/list", methods=["GET"])
@login_required
@permission_required
def menu_list():
    """获取菜单列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    menu_id    |    True    |    Int   |    菜单ID    |
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
    menu_id = int(request.args.get("menu_id")) if request.args.get("menu_id") else ""
    if menu_id:
        res = Menu.query.filter_by(id=menu_id).all()
        total = 1
    else:
        total = Menu.query.count()
        if key_word:
            res = Menu.query.filter(Menu.menu_name.ilike('%' + key_word + "%")).order_by(Menu.addtime.desc()).paginate(
                page=page, per_page=per_page)
            total = Menu.query.filter(Menu.menu_name.ilike('%' + key_word + "%")).count()
        else:
            res = Menu.query.order_by(Menu.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route('/menu/del/<int:menu_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
def menu_delete(menu_id):
    """删除菜单

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    menu_id    |    false    |    Int   |    菜单ID    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    menu_id = menu_id
    res = Menu.query.filter_by(id=menu_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

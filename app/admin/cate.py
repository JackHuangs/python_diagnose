#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/4/15 19:10
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : cate.py
# @Software: PyCharm
import os
from . import admin
from flask import request, jsonify
from app.models import Cate
from app.admin.common.utils import file_rename, allowed_file
from app.admin.db import db
from app.admin.common.utils import dict_to_json
from app.admin.common.Auth import login_required

UPLOAD_FILE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(UPLOAD_FILE, 'images/cate/')
STATIC_URL = "http://127.0.0.1:5000/static/cate/"


@admin.route('cate/upload', methods=["POST"])
@login_required  # 必须登录的装饰器校验
def cate_upload():
    """上传分类图标

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    file    |    false    |    File   |    上传的文件字段名    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            new_filename = file_rename(file.filename, "cate")
            file.save(os.path.join(UPLOAD_FOLDER, new_filename))
            src = STATIC_URL + new_filename
        else:
            return jsonify({"status": 201, "msg": "error, please upload the correct type"})
        return jsonify({"status": 200, "msg": "上传成功", "src": src})
    else:
        return jsonify({"status": 202, "msg": "GET不支持"})


@admin.route('cate/add', methods=["POST"])
@login_required  # 必须登录的装饰器校验
def cate_add():
    """添加分类

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    name    |    False    |    String   |     昵称    |
    |    icon    |    False    |    String   |     图标    |
    |    desc    |    True    |    String   |    描述    |
    |    is_index    |    True    |    Int   |    置顶首页    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    name = request.form.get("name")
    icon = request.form.get("icon")
    desc = request.form.get("desc") if request.form.get("desc") else None
    is_index = request.form.get("is_index") if request.form.get("is_index") else 1
    if name is None and icon is None:
        return jsonify({
            "status": 201,
            "msg": "分类名或图标不能为空"
        })
    else:
        res = Cate(name=name, icon=icon, desc=desc, is_index=is_index)
        db.session.add(res)
        db.session.commit()
        return jsonify({
            "name": res.name,
            "status": 200,
            "msg": "添加成功"
        })


@admin.route("cate/list", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def cate_list():
    """获取分类列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    cate_id    |    True    |    Int   |    ID    |
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
    cate_id = int(request.args.get("cate_id")) if request.args.get("cate_id") else ""
    if cate_id:
        res = Cate.query.filter_by(id=cate_id).all()
        total = 1
    else:
        total = Cate.query.count()
        if key_word:
            res = Cate.query.filter(Cate.name.ilike('%' + key_word + "%")).order_by(Cate.addtime.desc()).paginate(
                page=page, per_page=per_page)
            total = Cate.query.filter(Cate.name.ilike('%' + key_word + "%")).count()
        else:
            res = Cate.query.order_by(Cate.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route("cate/all", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def cate_all():
    """获取全部分类（不分页）

    @@@
    #### args

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    total = Cate.query.count()
    res = Cate.query.all()
    return dict_to_json(res, total)


@admin.route("cate/edit/<int:cate_id>", methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
def cate_edit(cate_id):
    """编辑分类

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    cate_id    |    False    |    String   |    Id    |
    |    name    |    False    |    String   |     昵称    |
    |    icon    |    False    |    String   |     图标    |
    |    desc    |    True    |    String   |    描述    |
    |    is_index    |    True    |    Int   |    置顶首页    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    cate_id = cate_id
    res = Cate.query.filter_by(id=cate_id).first()
    name = request.form.get("name") if request.form.get("name") else res.name
    icon = request.form.get("icon") if request.form.get("icon") else res.icon
    desc = request.form.get("desc") if request.form.get("desc") else res.desc
    is_index = request.form.get("is_index") if request.form.get("is_index") else res.is_index
    res.name = name
    res.icon = icon
    res.desc = desc
    res.is_index = is_index
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})


@admin.route('/cate/del/<int:cate_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
def cate_delete(cate_id):
    """删除分类

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    cate_id    |    false    |    Int   |    ID    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    cate_id = cate_id
    res = Cate.query.filter_by(id=cate_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

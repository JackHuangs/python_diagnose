#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/4/15 15:43
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : banner.py
# @Software: PyCharm
import os
from . import admin
from flask import request, jsonify
from app.models import Banner
from app.admin.common.utils import file_rename, allowed_file
from app.admin.db import db
from app.admin.common.utils import dict_to_json
from app.admin.common.Auth import login_required

UPLOAD_FILE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(UPLOAD_FILE, 'images/banner/')
STATIC_URL = "http://127.0.0.1:5000/static/banner/"


@admin.route('banner/upload', methods=["POST"])
@login_required  # 必须登录的装饰器校验
def banner_upload():
    """上传banner图片

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
            new_filename = file_rename(file.filename, "banner")
            file.save(os.path.join(UPLOAD_FOLDER, new_filename))
            src = STATIC_URL + new_filename
        else:
            return jsonify({"status": 201, "msg": "error, please upload the correct type"})
        return jsonify({"status": 200, "msg": "上传成功", "src": src})
    else:
        return jsonify({"status": 202, "msg": "GET不支持"})


@admin.route('banner/add', methods=["POST"])
@login_required  # 必须登录的装饰器校验
def banner_add():
    """添加banner

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    name    |    False    |    String   |     昵称    |
    |    desc    |    True    |    String   |    描述    |
    |    path    |    True    |    Int   |    图片地址    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    name = request.form.get("name") if request.form.get("name") else None
    desc = request.form.get("desc") if request.form.get("desc") else None
    path = request.form.get("path")
    if path is None:
        return jsonify({
            "status": 201,
            "msg": "图片不能为空"
        })
    else:
        res = Banner(name=name, desc=desc, path=path)
        db.session.add(res)
        db.session.commit()
        return jsonify({
            "name": res.name,
            "status": 200,
            "msg": "添加成功"
        })


@admin.route("banner/list", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def banner_list():
    """获取banner列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    banner_id    |    True    |    Int   |    ID    |
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
    banner_id = int(request.args.get("id")) if request.args.get("id") else ""
    if banner_id:
        res = Banner.query.filter_by(id=banner_id).all()
        total = 1
    else:
        total = Banner.query.count()
        if key_word:
            res = Banner.query.filter(Banner.name.ilike('%' + key_word + "%")).order_by(Banner.addtime.desc()).paginate(
                page=page, per_page=per_page)
            total = Banner.query.filter(Banner.name.ilike('%' + key_word + "%")).count()
        else:
            res = Banner.query.order_by(Banner.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route("banner/all", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def banner_all():
    """获取全部banner（不分页）

    @@@
    #### args

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    total = Banner.query.count()
    res = Banner.query.all()
    return dict_to_json(res, total)


@admin.route("banner/edit/<int:banner_id>", methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
def banner_edit(banner_id):
    """编辑banner

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |        |    False    |    Int   |    菜单ID    |
    |    banner_id    |    False    |    String   |    Id    |
    |    name    |    False    |    String   |     昵称    |
    |    desc    |    True    |    String   |    描述    |
    |    path    |    True    |    Int   |    图片地址    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    banner_id = banner_id
    res = Banner.query.filter_by(id=banner_id).first()
    name = request.form.get("name") if request.form.get("name") else res.name
    desc = request.form.get("desc") if request.form.get("desc") else res.desc
    path = request.form.get("path") if request.form.get("path") else res.path
    res.name = name
    res.desc = desc
    res.path = path
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})


@admin.route('/banner/del/<int:banner_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
def banner_delete(banner_id):
    """删除banner

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    banner_id    |    false    |    Int   |    ID    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    banner_id = banner_id
    res = Banner.query.filter_by(id=banner_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

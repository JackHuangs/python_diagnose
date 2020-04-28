#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 0:10
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : disease.py
# @Software: PyCharm
import os
from . import admin
from flask import request, jsonify
from app.models import Disease
from app.admin.common.utils import file_rename, allowed_file
from app.admin.db import db
from app.admin.common.utils import dict_to_json
from app.admin.common.Auth import login_required

UPLOAD_FILE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(UPLOAD_FILE, 'images/disease/')
STATIC_URL = "http://127.0.0.1:5000/static/disease/"


@admin.route('disease/upload', methods=["POST"])
@login_required  # 必须登录的装饰器校验
def disease_uploads():
    """上传疾病图片

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
            new_filename = file_rename(file.filename, "disease")
            file.save(os.path.join(UPLOAD_FOLDER, new_filename))
            src = STATIC_URL + new_filename
        else:
            return jsonify({"status": 201, "msg": "error, please upload the correct type"})
        return jsonify({"status": 200, "msg": "上传成功", "src": src})
    else:
        return jsonify({"status": 202, "msg": "GET不支持"})


@admin.route('disease/add', methods=["POST"])
@login_required  # 必须登录的装饰器校验
def disease_add():
    """添加疾病

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    name    |    False    |    String   |    名字    |
    |    is_index   |    True    |    String   |    指定首页     |
    |    desc    |    True    |    String   |    描述    |
    |    cate_id    |    True    |    Int   |    分类ID    |
    |    photo    |    True    |    Int   |    图片地址    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    name = request.form.get("name")
    is_index = request.form.get("is_index") if request.form.get("is_index") else 1
    desc = request.form.get("desc") if request.form.get("desc") else None
    cate_id = request.form.get("cate_id") if request.form.get("cate_id") else 0
    photo = request.form.get("photo") if request.form.get("photo") else None
    if name is None:
        return jsonify({
            "status": 201,
            "msg": "疾病名不能为空"
        })
    elif Disease.query.filter_by(name=name).first() is not None:
        return jsonify({
            "status": 202,
            "msg": "疾病名已存在"
        })
    else:
        res = Disease(name=name, is_index=is_index, desc=desc, photo=photo, cate_id=cate_id)
        db.session.add(res)
        db.session.commit()
        return jsonify({
            "name": res.name,
            "status": 200,
            "msg": "添加成功"
        })


@admin.route("disease/list", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def disease_list():
    """获取疾病列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    disease_id    |    True    |    Int   |    ID    |
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
    disease_id = int(request.args.get("disease_id")) if request.args.get("disease_id") else ""
    cate_id = int(request.args.get("cate_id")) if request.args.get("cate_id") else ""
    if disease_id:
        res = Disease.query.filter_by(id=disease_id).all()
        total = 1
    elif cate_id:
        total = Disease.query.filter_by(cate_id=cate_id).count()
        res = Disease.query.filter_by(cate_id=cate_id).all()
    else:
        total = Disease.query.count()
        if key_word:
            res = Disease.query.filter(Disease.name.ilike('%' + key_word + "%")).order_by(Disease.addtime.desc()).paginate(
                page=page, per_page=per_page)
            total = Disease.query.filter(Disease.name.ilike('%' + key_word + "%")).count()
        else:
            res = Disease.query.order_by(Disease.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route("disease/all", methods=["GET"])
@login_required  # 必须登录的装饰器校验
def disease_all():
    """获取全部疾病（不分页）

    @@@
    #### args

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    total = Disease.query.count()
    res = Disease.query.all()
    return dict_to_json(res, total)


@admin.route("disease/edit/<int:disease_id>", methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
def disease_edit(disease_id):
    """编辑疾病

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |        |    False    |    Int   |    菜单ID    |
    |    disease_id    |    False    |    String   |    Id    |
    |    name    |    False    |    String   |    名字    |
    |    is_index    |    True    |    String   |    指定首页     |
    |    desc    |    True    |    String   |    描述    |
    |    cate_id    |    True    |    Int   |    分类ID    |
    |    photo    |    True    |    Int   |    图片地址    |
    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    disease_id = disease_id
    res = Disease.query.filter_by(id=disease_id).first()
    name = request.form.get("name") if request.form.get("name") else res.name
    is_index = request.form.get("is_index") if request.form.get("is_index") else res.is_index
    desc = request.form.get("desc") if request.form.get("desc") else res.desc
    cate_id = request.form.get("cate_id") if request.form.get("cate_id") else res.cate_id
    photo = request.form.get("photo") if request.form.get("photo") else res.photo
    res.name = name
    res.is_index = is_index
    res.desc = desc
    res.cate_id = cate_id
    res.photo = photo
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})


@admin.route('/disease/del/<int:disease_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
def disease_delete(disease_id):
    """删除疾病

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    disease_id    |    false    |    Int   |    ID    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    disease_id = disease_id
    res = Disease.query.filter_by(id=disease_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

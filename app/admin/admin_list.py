#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 20:10
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : admin_list.py
# @Software: PyCharm
from . import admin
from app.models import Admin
from app.admin.common.Auth import login_required, permission_required
from app.admin.common.utils import dict_to_json
from flask import request, jsonify
from app.admin.db import db


@admin.route('/admin/list', methods=["GET"])
@login_required  # 必须登录的装饰器校验
@permission_required
def admin_list():
    """查询管理员列表

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    admin_id    |    True    |    Int   |    管理员ID    |
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
    admin_id = int(request.args.get("admin_id")) if request.args.get("admin_id") else ""
    if admin_id:
        res = Admin.query.filter_by(id=admin_id).all()
        total = 1
    else:
        total = Admin.query.count()
        if key_word:
            res = Admin.query.filter(Admin.name.ilike('%' + key_word + "%")).order_by(Admin.addtime.desc()).paginate(
                page=page, per_page=per_page)
            total = Admin.query.filter(Admin.name.ilike('%' + key_word + "%")).count()
        else:
            res = Admin.query.order_by(Admin.addtime.desc()).paginate(page=page, per_page=per_page)
        res = res.items
    return dict_to_json(res, total)


@admin.route('/admin/edit/<int:admin_id>', methods=["PUT", "PATCH"])
@login_required  # 必须登录的装饰器校验
@permission_required
def admin_edit(admin_id):
    """修改管理员信息

        @@@
        #### args

        | args | nullable | type | remark |
        |--------|--------|--------|--------|
        |    admin_id    |    False    |    Int   |    管理员ID    |
        |    name    |    True    |    String   |    用户名    |
        |    pwd    |    True    |    String   |    密码    |
        |    is_super    |    True    |    0or1   |    超级管理员    |

        #### return
        - ##### json
        > {"msg": "success", "code": 200}
        @@@
        """
    admin_id = admin_id
    res = Admin.query.filter_by(id=admin_id).first()
    name = request.form.get('name') if request.form.get('name') else res.name
    is_super = request.form.get('is_super') if request.form.get('is_super') else res.is_super
    role_id = request.form.get('role_id') if request.form.get('role_id') else res.role_id
    res.hash_password(request.form.get('pwd')) if request.form.get('pwd') else res.pwd
    res.is_super = is_super
    res.role_id = role_id
    res.name = name
    db.session.commit()
    return jsonify({"status": 200, "msg": "修改成功"})


@admin.route('/admin/del/<int:admin_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
@permission_required
def admin_delete(admin_id):
    """删除管理员

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    admin_id    |    false    |    Int   |    管理员ID    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    admin_id = admin_id
    res = Admin.query.filter_by(id=admin_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

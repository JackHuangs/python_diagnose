#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:49
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : user_profile_del.py
# @Software: PyCharm
from . import admin
from flask import jsonify
from app.models import User
from app.admin.db import db
from app.admin.common.Auth import login_required, permission_required


@admin.route('/user/del/<int:user_id>', methods=["DELETE"])
@login_required  # 必须登录的装饰器校验
def user_profile_del(user_id):
    """删除用户

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    user_id    |    false    |    Int   |    用户ID    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    user_id = user_id
    res = User.query.filter_by(id=user_id).first()
    db.session.delete(res)
    db.session.commit()
    return jsonify({"status": 200, "msg": "删除成功"})

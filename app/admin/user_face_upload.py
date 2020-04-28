#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 18:57
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : user_face_upload.py
# @Software: PyCharm
import os
from . import admin
from flask import request, jsonify
from app.models import Userpto
from app.admin.db import db
from app.admin.common.utils import file_rename, allowed_file
from app.admin.common.Auth import login_required
from app.admin.common.user_face_process import face_detect_demo as faces


UPLOAD_FILE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(UPLOAD_FILE, 'images/upload/')
STATIC_URL = "http://127.0.0.1:5000/static/upload/"


@admin.route("/upload", methods=['POST'])
@login_required  # 必须登录的装饰器校验
def uploads():
    """上传诊断图片

    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    file    |    false    |    File   |    上传的文件字段名    |
    |    user_id    |    false    |    Int   |    用户ID    |

    #### return
    - ##### json
    > {"msg": "success", "code": 200}
    @@@
    """
    if request.method == 'POST':
        file = request.files['file']
        user_id = request.form.get('user_id')
        if file and allowed_file(file.filename):
            new_filename = file_rename(file.filename, "upload")
            file.save(os.path.join(UPLOAD_FOLDER, new_filename))
            file_src = UPLOAD_FOLDER + new_filename
            user_pto_url = STATIC_URL + new_filename
            organs = faces(file_src)
            if organs["face"] is None:
                return jsonify({"status": 203, "msg": "请重新上传"})
            else:
                res = Userpto(user_id=user_id,
                              user_pto_url=user_pto_url,
                              face_pto_url=organs["face"],
                              left_eye_pto_url=organs["left_eye"],
                              right_eye_pto_url=organs["right_eye"],
                              nose_pto_url=organs["nose"],
                              tongue_pto_url=organs["tongue"])
                db.session.add(res)
                db.session.commit()
                return jsonify({"status": 200, "msg": "上传成功"})
        else:
            return jsonify({"status": 201, "msg": "error, please upload the correct type"})

    else:
        return jsonify({"status": 202, "msg": "GET不支持"})

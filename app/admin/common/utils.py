#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 17:56
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : utils.py
# @Software: PyCharm
import time
import uuid
from pypinyin import lazy_pinyin
from flask import jsonify
from werkzeug.utils import secure_filename

ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


# format the date to timestamp
def datetime_to_timestamp(datetime):
    return time.mktime(datetime.timetuple())


# data by db to dict then to list
def dict_to_json(data, total=None):
    if len(data):
        users_list = {}
        users_list["data"] = []
        users_list["total"] = total
        for user in data:
            dictret = dict(user.__dict__)
            if "pwd" in dictret:
                dictret.pop("pwd")
            dictret.pop('_sa_instance_state', None)
            if "addtime" in dictret:
                dictret["timestamp"] = datetime_to_timestamp(dictret["addtime"])
            users_list["data"].append(dictret)
        users_list["status"] = 200
        return jsonify(users_list)
    else:
        return jsonify({"status": 200, "msg": "数据为空", "total": 0})


# rename the photo file name
def file_rename(filename, types=None):
    file_name = secure_filename(''.join(lazy_pinyin(filename)))
    ext = file_name.rsplit('.', 1)[1]
    unix_time = int(time.time())
    new_filename = types + '_' + str(unix_time) + str(uuid.uuid4().hex) + '.' + ext
    return new_filename


# limit the file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS





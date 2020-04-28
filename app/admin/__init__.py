#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 19:04
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

admin = Blueprint("admin", __name__)

from . import views
from . import operation_log
from . import admin_login
from . import admin_register
from . import admin_list
from . import user_profile_list
from . import user_profile_edit
from . import user_profile_del
from . import user_diagnosis_pto
from . import user_face_upload
from . import wechat_login
from . import super_admin_auth
from . import role_auth
from . import admin_pwd_edit
from . import menu_list
from . import disease
from . import banner
from . import cate


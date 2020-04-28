#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 19:02
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Flask
from flask_cors import CORS
from flask_docs import ApiDoc

# set the static path
app = Flask(__name__, static_folder='admin/images', static_url_path="/static")

# set the token secret_key
app.config['SECRET_KEY'] = 'programmer will change and rebuild the world'

# Api Document needs to be displayed
app.config['API_DOC_MEMBER'] = ['api']
ApiDoc(app)

# resolve CROS
CORS(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/api")

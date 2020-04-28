#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 11:30
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : manager.py
# @Software: PyCharm
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# connect the mysql
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@127.0.0.1:3306/diagnosis"
# track the change
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# auto commit after request database
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

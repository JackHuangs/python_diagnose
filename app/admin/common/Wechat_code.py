#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 17:49
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : Wechat_code.py
# @Software: PyCharm
import requests


# get the wechat openid and session_key by code
def get_code(code):
    code = code
    appid = "wx98b14393dfd7affc"
    secret = "c7b1ace235f43202c9aedca19580dc7b"
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'.format(
        appid=appid, secret=secret, code=code)
    res = requests.get(url)
    return res.json().get('openid')


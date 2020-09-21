# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:21
# @Author  : xhb
# @FileName: gift.py
# @Software: PyCharm


from flask import render_template
from sqlalchemy import desc, func
from . import web
from app.service.gift import GiftService


@web.route('/my/gifts')
def my_gifts():
    pass
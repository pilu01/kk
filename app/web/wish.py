# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:23
# @Author  : xhb
# @FileName: wish.py
# @Software: PyCharm


from flask import render_template
from sqlalchemy import desc, func
from . import web
from app.service.gift import GiftService


@web.route('/my/wish')
def my_wish():
    pass
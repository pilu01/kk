# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:26
# @Author  : xhb
# @FileName: drift.py
# @Software: PyCharm


from flask import render_template
from sqlalchemy import desc, func
from . import web
from app.service.gift import GiftService


@web.route('/pending')
def pending():
    pass
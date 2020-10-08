# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:26
# @Author  : xhb
# @FileName: drift.py
# @Software: PyCharm


from flask import render_template
from flask_login import login_required
from sqlalchemy import desc, func
from . import web
from app.service.gift import GiftService


@web.route('/pending')
def pending():
    pass




@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    pass
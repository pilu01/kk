# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 16:37
# @Author  : xhb
# @FileName: main.py
# @Software: PyCharm
from . import web
from app.service.gift import GiftService
from flask import render_template


@web.route('/')
def index():
    """
        首页视图函数
        这里使用了缓存，注意缓存必须是贴近index函数的
    """
    gift_list = GiftService.recent()
    return render_template('index.html', recent=gift_list)

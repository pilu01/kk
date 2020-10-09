# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 16:37
# @Author  : xhb
# @FileName: main.py
# @Software: PyCharm
from . import web
from app.models.gift import Gift
from flask import render_template
from app.view_models.book import BookViewModel


@web.route('/')
def index():
    """
        首页视图函数
        这里使用了缓存，注意缓存必须是贴近index函数的
    """
    gift_list = Gift.recent()
    books = [BookViewModel(gift.book) for gift in gift_list]
    return render_template('index.html', recent=books)

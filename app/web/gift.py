# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:21
# @Author  : xhb
# @FileName: gift.py
# @Software: PyCharm
from flask import render_template, flash, url_for, redirect,current_app
from sqlalchemy import desc, func

from . import web
from flask_login import login_required, current_user
from app import db
from ..models.gift import Gift
from app.view_models.gift import MyGifts

@login_required
@web.route('/my/gifts')
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    gift_isbns = [gift.isbn for gift in gifts_of_mine]
    count_list = Gift.get_wish_count(gift_isbns)
    view_model = MyGifts(gifts_of_mine, count_list).gifts
    return render_template('my_gifts.html', gifts=view_model)


@login_required
@web.route('/gifts/book/<isbn>')
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        gift = Gift()
        gift.isbn = isbn
        gift.uid = current_user.id
        db.session.add(gift)
        db.session.commit()
        current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
    else:
        flash("这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加")

    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    pass

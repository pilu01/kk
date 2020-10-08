# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:23
# @Author  : xhb
# @FileName: wish.py
# @Software: PyCharm


from flask import render_template, current_app, flash, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy import desc, func

from . import web
from app.service.gift import GiftService
from app.models.wish import Wish
from .. import db


@login_required
@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    wishes = Wish.query.filter_by(uid=uid, launched=False).all()



@login_required
@web.route('/wish/book/<isbn>')
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加")

    return redirect(url_for('web.book_detail', isbn=isbn))

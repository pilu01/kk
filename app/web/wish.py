# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:23
# @Author  : xhb
# @FileName: wish.py
# @Software: PyCharm


from flask import render_template, current_app, flash, url_for, redirect
from flask_login import current_user, login_required

from . import web
from app.models.wish import Wish
from .. import db
from app.view_models.wish import MyWishes


@login_required
@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.my_wishes(uid)
    wish_isbns = [wish.isbn for wish in wishes_of_mine]
    count_list = Wish.get_gift_count(wish_isbns)
    view_model = MyWishes(wishes_of_mine, count_list).wishes
    return render_template('my_wish.html', wishes=view_model)


@login_required
@web.route('/wish/book/<isbn>')
def satisfy_wish():
    pass

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

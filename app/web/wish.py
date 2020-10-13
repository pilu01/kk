# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:23
# @Author  : xhb
# @FileName: wish.py
# @Software: PyCharm


from flask import render_template, current_app, flash, url_for, redirect
from flask_login import current_user, login_required

from . import web
from app.models.wish import Wish
from app.models.gift import Gift
from .. import db
from app.view_models.wish import MyWishes
from app.libs.mail import send_mail


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
@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    """
            向想要这本书的人发送一封邮件
            注意，这个接口需要做一定的频率限制
            这接口比较适合写成一个ajax接口
        """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email, '有人想送你一本书', 'email/satisify_wish', wish=wish,
                   gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


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


@login_required
@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
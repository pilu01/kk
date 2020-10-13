# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:26
# @Author  : xhb
# @FileName: drift.py
# @Software: PyCharm
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc, func, or_
from . import web
from app.models.drift import Drift
from app.models.gift import Gift
from app.forms.book import DriftForm
from app.models.base import db
from app.libs.mail import send_mail
from app.view_models.drift import DriftCollection
from app.libs.enums import PendingStatus
from app.models.user import User
from app.models.wish import Wish

@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    # 检查是否是自己的书
    if current_gift.is_yourself_gift(current_user.id):
        flash("这本书是你自己的，不要向自己索要书籍")
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    # 检查鱼豆数量，每索要两本书，自己必须赠送一本
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                             wisher=current_user,
                             gift=current_gift)

        return redirect(url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, form=form, user_beans=current_user.beans)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.requester_id==current_user.id,
                                   Drift.gifter_id == current_user.id)
                                ).order_by(desc(Drift.create_time)).all()

    view_model = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=view_model.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
        拒绝请求，只有书籍赠送者才能拒绝请求
        注意需要验证超权
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, gifter_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """
        撤销请求，只有书籍请求者才可以撤销请求
        注意需要验证超权
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, requester_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    """
        确认邮寄，只有书籍赠送者才可以确认邮寄
        注意需要验证超权
    """
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.success
        current_user.beans += current_app.config['BEANS_EVERY_DRIFT']
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        # 不查询直接更新;这一步可以异步来操作
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # 从form里copy数据到 drift
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id
        drift.book_title = current_gift.book.title
        drift.book_author = current_gift.book.author_str
        drift.book_img = current_gift.book.image_large
        current_user.beans -= 1

        db.session.add(drift)

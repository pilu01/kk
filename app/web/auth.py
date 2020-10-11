# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 14:33
# @Author  : xhb
# @FileName: auth.py
# @Software: PyCharm

from . import web
from app.forms.auth import RegisterForm, LoginForm, EmailForm
from flask_login import login_user, login_required, logout_user, current_user
from flask import request, redirect, url_for, render_template, flash
from app.models.user import User
from app.models import db


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()

        login_user(user, False)
        return redirect(url_for('web.index'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password/', methods=['GET', 'POST'])
def forget_password_request():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            account_email = form.email.data
            user_account = User.query.filter_by(email=account_email).first_or_404()
            from app.libs.mail import send_mail
            send_mail(user_account, "重置密码", "email/reset_password.html", user=current_user, token='12345')
    return render_template('auth/forget_password_request.html')


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    return render_template('auth/forget_password.html')



@web.route('/', methods=['GET', 'POST'])
def personal_center():
    pass


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))
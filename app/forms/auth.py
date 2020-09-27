# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 14:40
# @Author  : xhb
# @FileName: auth.py
# @Software: PyCharm


from wtforms import StringField, IntegerField, Form, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, length, Email, ValidationError
from app.models.user import User


class EmailForm(Form):
    email = StringField('电子邮件', validators=[DataRequired(), length(1, 64), Email(message='电子邮箱不符合规范')])


class RegisterForm(EmailForm):
    nickname = StringField('昵称', validators=[DataRequired(), length(2, 10, message='昵称至少需要两个字符，最多10个字符')])
    password = StringField('密码', validators=[DataRequired(), length(6, 20)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class LoginForm(EmailForm):
    password = PasswordField('密码', validators=[DataRequired(message='密码不可以为空，请输入你的密码')])
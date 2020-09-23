# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 14:39
# @Author  : xhb
# @FileName: book.py
# @Software: PyCharm


from wtforms import StringField, IntegerField, Form
from wtforms.validators import Length, NumberRange


class SearchForm(Form):
    q = StringField(validators=[Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)




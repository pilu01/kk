# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 14:25
# @Author  : xhb
# @FileName: __init__.py.py
# @Software: PyCharm

from flask import Blueprint, url_for


web = Blueprint('web', __name__, template_folder='templates')


from app.web import book
from app.web import main
from app.web import gift
from app.web import wish
from app.web import drift
from app.web import auth


# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 14:14
# @Author  : xhb
# @FileName: __init__.py.py
# @Software: PyCharm

"""
创建应用程序，并注册相关蓝图
"""
from app.models.base import db
from flask_login import LoginManager
from flask import Flask


# login_manager = LoginManager()


def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)



def create_app():
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object('app.settings')
    app.config.from_object('app.secure')

    # 注册login 模块
    # login_manager.init_app(app)
    # login_manager.login_view = 'web.login'
    # login_manager.login_message = '请先登录或注册'

    # 注册SQLAlchemy
    db.init_app(app)


    # register_api_blueprint(app)
    register_web_blueprint(app)

    return app




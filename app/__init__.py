# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 14:14
# @Author  : xhb
# @FileName: __init__.py.py
# @Software: PyCharm

"""
创建应用程序，并注册相关蓝图
"""


from flask import Flask



def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)



def create_app():
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object('app.settings')
    app.config.from_object('app.secure')

    # register_api_blueprint(app)
    register_web_blueprint(app)

    return app




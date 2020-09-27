# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 14:14
# @Author  : xhb
# @FileName: fisher.py
# @Software: PyCharm

from app import create_app, db
from app.models import book, user, wish, gift




app = create_app()

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    # 如果要使用vscode调试，需要将debug设置为False，否则无法命中请求断点
    app.run(host='0.0.0.0', debug=True)
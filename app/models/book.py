# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 15:38
# @Author  : xhb
# @FileName: book.py
# @Software: PyCharm


import json
from app.models.base import Base, db


class Book(Base):
    """
        一些属性定义重复性比较大，元类可以解决这个问题
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    _author = db.Column('author', db.String(30), default='未名')
    binding = db.Column(db.String(20))
    publisher = db.Column(db.String(50))
    price = db.Column(db.String(20))
    pages = db.Column(db.Integer)
    pubdate = db.Column(db.String(20))
    isbn = db.Column(db.String(15), nullable=False, unique=True)
    summary = db.Column(db.String(1000))
    image = db.Column(db.String(50))

    # @property
    # def author(self):
    #     return self._author if not self._author else json.loads(self._author)

    # @author.setter
    # def author(self, value):
    #     if not isinstance(value, str):
    #         self._author = json.dumps(value, ensure_ascii=False)
    #     else:
    #         self._author = value

    @property
    def author_str(self):
        return '' if not self._author else '、'.join(self._author)





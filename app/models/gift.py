# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 16:42
# @Author  : xhb
# @FileName: gift.py
# @Software: PyCharm
from app.spider.yushu_book import YuShuBook
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models import db


class Gift(Base):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = db.Column(db.String(13))
    launched = db.Column(db.Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book
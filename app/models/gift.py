# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 16:42
# @Author  : xhb
# @FileName: gift.py
# @Software: PyCharm
from app.spider.yushu_book import YuShuBook
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models import db
from sqlalchemy import desc, func
from flask import current_app
from app.models.wish import Wish
from collections import namedtuple


EachGiftWishCount = namedtuple('EachGiftWishCount', ['isbn', 'count'])

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
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = cls.query.filter_by(uid=uid, launched=False).order_by(
            desc(cls.create_time)
        ).all()
        return gifts

    @classmethod
    def recent(cls):
        gift_list = cls.query.filter_by(launched=False).group_by(
            cls.isbn
        ).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).distinct().all()

        return gift_list

    @classmethod
    def get_wish_count(cls, isbn_list):
        count_list = db.session.query(Wish.isbn, func.count(Wish.id)).filter(
            Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 1
        ).group_by(Wish.isbn).all()

        count_list = [EachGiftWishCount(w[0], w[1]) for w in count_list]
        return count_list


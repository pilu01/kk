# -*- coding: utf-8 -*-
# @Time    : 2020/9/24 9:32
# @Author  : xhb
# @FileName: wish.py
# @Software: PyCharm


from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models import db



class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def my_wishes(cls, uid):
        wishes = cls.query.filter_by(uid=uid, launched=False).order_by(
            desc(cls.create_time)
        ).all()
        return wishes

    @classmethod
    def get_gift_count(cls, isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(Gift.isbn, func.count(Gift.id)).filter(
            Gift.launched == False, Gift.isbn.in_(isbn_list), Gift.status == 1
        ).group_by(Gift.isbn).all()

        data = [{'isbn': w[0], 'count': w[1]} for w in count_list]
        return data

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
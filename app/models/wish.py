# -*- coding: utf-8 -*-
# @Time    : 2020/9/24 9:32
# @Author  : xhb
# @FileName: wish.py
# @Software: PyCharm


from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)
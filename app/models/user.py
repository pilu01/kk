# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 14:59
# @Author  : xhb
# @FileName: user.py
# @Software: PyCharm


from app.models.base import Base
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import String, Unicode, DateTime, Boolean
from sqlalchemy import SmallInteger, Integer, Float
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    gifts = relationship('Gift')


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
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(100))

    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    # gifts = relationship('Gift')

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    # def __init__(self, nickname, email, password, phone_number=None):
    #     self.nickname = nickname
    #     self._password = generate_password_hash(password)
    #     self.email = email
    #     self.phone_number = phone_number
    #     super(User, self).__init__()


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))

# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 15:37
# @Author  : xhb
# @FileName: base.py
# @Software: PyCharm


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from contextlib import contextmanager
from flask import current_app


__all__ = ['db', 'Base']


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if "status" not in kwargs:
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = db.Column('create_time', db.Integer)
    status = db.Column(db.SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def save(self):
        db.session.add(self)
        db.session.commit()



class BaseNoCreateTime(db.Model):
    __abstract__ = True
    status = db.Column(db.SmallInteger, default=1)














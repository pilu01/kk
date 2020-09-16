# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 15:07
# @Author  : xhb
# @FileName: gift.py
# @Software: PyCharm


from app.models.gift import Gift
from app.view_models.book import BookViewModel
from flask import current_app
from sqlalchemy import func, desc
from app.models import db
from app.models.wish import Wish


class GiftService:
    """
    gift server 层
    """
    @staticmethod
    def recent():
        gift_list = Gift.query.filter_by(launched=False).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).all()
        books = [BookViewModel(gift.book.first) for gift in gift_list]
        return books
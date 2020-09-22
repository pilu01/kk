# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 14:30
# @Author  : xhb
# @FileName: book.py
# @Software: PyCharm
from . import web
from app.forms.book import SearchForm
from flask import request, flash, render_template, jsonify, redirect, url_for
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection
from app.models.book import Book
from app.models import db

from app.models.gift import Gift
from app.models.wish import Wish

@web.route('/book/search', methods=['Get', 'POST'])
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        if isbn_or_key == 'isbh':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # for i in books.books:
        #     b = Book()
        #     b.set_attrs(i)
        #     db.session.add(b)
        # db.session.commit()
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    """
        1. 当书籍既不在心愿清单也不在礼物清单时，显示礼物清单
        2. 当书籍在心愿清单时，显示礼物清单
        3. 当书籍在礼物清单时，显示心愿清单
        4. 一本书要防止即在礼物清单，又在赠送清单，这种情况是不符合逻辑的

        这个视图函数不可以直接用cache缓存，因为不同的用户看到的视图不一样
        优化是一个逐步迭代的过程，建议在优化的初期，只缓存那些和用户无关的“公共数据"
    """
    has_in_gifts = False
    has_in_wishes = False
    # isbn_or_key = is_isbn_or_key(isbn)
    # if isbn_or_key == 'isbn':
    # 获取图书信息
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    book = BookViewModel(yushu_book.first)
    # if has_in_gifts:
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)
    return render_template('book_detail.html', book=book, has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)
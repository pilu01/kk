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
from app.view_models.book import BookCollection, BookViewModel
from app.models.book import Book

from app.models import db

# from app.models.gift import Gift
# from app.models.wish import Wish


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
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    return render_template('book_detail.html', book=book, wishes=[], gifts=[])

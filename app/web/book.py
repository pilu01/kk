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


@web.route('/book/search', methods=['Get', 'POST'])
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        # page = form.page.data
        page = 1
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        if isbn_or_key == 'isbh':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        b = Book()

        for d in yushu_book.books:
            d['_author'] = d['author']
            b.set_attrs(d)
            b._author = b.author_str
            db.session.add(b)
        db.session.commit()
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')

    # return render_template('search_result.html', books=books)
    return redirect(url_for('web.index'))
# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 15:26
# @Author  : xhb
# @FileName: yushu_book.py
# @Software: PyCharm
from app.libs.http import Http


class YuShuBook():
    """
    鱼书api提供数据
    """
    per_page = 15
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page):
        page = int(page)
        url = self.keyword_url.format(keyword, self.per_page, self.per_page * (page - 1))
        result = Http.get(url)
        self._fill_connection(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def _fill_connection(self, data):
        self.total = data['total']
        self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None






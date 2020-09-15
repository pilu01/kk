# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 14:44
# @Author  : xhb
# @FileName: helper.py
# @Software: PyCharm


def is_isbn_or_key(q):
    isbn_or_key = 'keyword'
    if len(q) == 13 and q.isdigit():
        isbn_or_key = 'isbh'
    elif '-' in q and len(q.replace('-', '')) == 10:
        isbn_or_key = 'isbh'
    return isbn_or_key


def get_isbn(data_dict):
    isbn = data_dict.get('isbn')
    if not isbn:
        isbn = data_dict.get('isbn13')
        if not isbn:
            isbn = data_dict.get('isbn10')
    return isbn
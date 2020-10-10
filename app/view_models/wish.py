# -*- coding: utf-8 -*-
# @Time    : 2020/10/10 16:39
# @Author  : xhb
# @FileName: wish.py
# @Software: PyCharm


from collections import namedtuple
from app.view_models.book import BookViewModel


MyWish = namedtuple('MyWish', ['id', 'book', 'gifts_count'])

class MyWishes():
    def __init__(self, wishes_of_mine, gift_count_list):
        self._wishes_of_mine = wishes_of_mine
        self._gift_count_list = gift_count_list

        self.wishes = self._parse()

    def _parse(self):
        tmp_wishes = []
        for wish in self._wishes_of_mine:
            my_wish = self._matching(wish)
            tmp_wishes.append(my_wish)
        return tmp_wishes

    def _matching(self, wish):
        count = 0
        for gift_count in self._gift_count_list:
            if gift_count.isbn == wish.isbn:
                count = gift_count.count
        my_wish = MyWish(wish.id, BookViewModel(wish.book), count)
        return my_wish
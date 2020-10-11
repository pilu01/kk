# @Time    : 2020/10/9 下午10:02

__author__ = 'xhb'
from collections import namedtuple
from app.view_models.book import BookViewModel


MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])

class MyGifts():
    def __init__(self, gifts_of_mine, wish_count_list):
        self._gifts_of_mine = gifts_of_mine
        self._wish_count_list = wish_count_list

        self.gifts = self._parse()

    def _parse(self):
        tmp_gifts = []
        for gift in self._gifts_of_mine:
            my_gift = self._matching(gift)
            tmp_gifts.append(my_gift)
        return tmp_gifts

    def _matching(self, gift):
        count = 0
        for wish_count in self._wish_count_list:
            if wish_count.isbn == gift.isbn:
                count = wish_count.count
        my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        return my_gift


# class MyGift():
#     def __init__(self, data):
#         pass

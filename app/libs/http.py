# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 15:31
# @Author  : xhb
# @FileName: http.py
# @Software: PyCharm
import requests


class Http(object):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def get(url, json_return=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if json_return else ''
        return r.json() if json_return else r.text


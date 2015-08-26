# coding=utf-8
from unittest import TestCase

__author__ = 'MuRui'

import urllib2
from urllib import urlencode


class TestUserHandler(TestCase):
    def test_put(self):
        data = {"user_id": "55d8285fb217c415946bb057", "name": "牟瑞",
                "photo": "http://www.iteye.com/upload/logo/user/611462/2a7902d8-3a48-3aa2-8c30-69e4e52870d6.jpg"}
        url = 'http://127.0.0.1:8090/user?'

        url = url + urlencode(data)

        print url

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'PUT'

        request = urllib2.urlopen(request)
        print request.read()

    def test_post(self):
        data = {"type": "2", "id": "18910062599",
                "pwd": "123456", "name": "天天向上",
                "photo": "http://www.iteye.com/upload/logo/user/611462/2a7902d8-3a48-3aa2-8c30-69e4e52870d6.jpg"}
        url = 'http://127.0.0.1:8090/user?'

        url = url + urlencode(data)

        print url

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'POST'

        request = urllib2.urlopen(request)
        print request.read()
# coding=utf-8
from unittest import TestCase

__author__ = 'murui'
import urllib2
from urllib import urlencode


class TestWordsHandler(TestCase):
    def test_get(self):
        data = {"user_id": "55d4404db217c46ed9ca2b7f", "type": "0"}
        url = 'http://127.0.0.1:8090/words?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'GET'
        request = urllib2.urlopen(request)
        print request.read()
        # self.fail()
from unittest import TestCase

__author__ = 'murui'
import json
import urllib2


class TestUserSearchHandler(TestCase):
    def test_get(self):
        url = 'http://127.0.0.1:8090/user/search'
        values = {'user': 'Smith'}

        jdata = json.dumps(values)
        request = urllib2.Request(url, jdata)
        request.get_method = lambda: 'get'  # 设置HTTP的访问方式
        request = urllib2.urlopen(request)
        print request.read()

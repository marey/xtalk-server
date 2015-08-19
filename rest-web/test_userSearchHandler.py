from unittest import TestCase

__author__ = 'murui'
import json
import urllib2


class TestUserSearchHandler(TestCase):
    def test_get(self):
        url = 'http://127.0.0.1:8090/user?type=2&id=13800138000&pwd=1111111'
        # values = {'type': '2', "id": "13800138000", "pwd": "11111"}

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'POST'
        request = urllib2.urlopen(request)
        print request.read()

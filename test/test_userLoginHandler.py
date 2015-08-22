from unittest import TestCase

__author__ = 'MuRui'

import urllib2
from urllib import urlencode


class TestUserLoginHandler(TestCase):
    def test_post(self):
        data = {"id": "test", "type": "2"}
        url = 'http://127.0.0.1:8090/user/login?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'POST'
        request = urllib2.urlopen(request)
        print request.read()
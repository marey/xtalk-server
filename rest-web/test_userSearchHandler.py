# coding=utf-8
from unittest import TestCase

__author__ = 'murui'
import json
import urllib2
from urllib import urlencode
from model import *
import  utils


class TestUserSearchHandler(TestCase):
    def test_get(self):
        # url = 'http://127.0.0.1:8090/user?type=2&id=13800138000&pwd=1111111'
        # values = {'type': '2', "id": "13800138000", "pwd": "11111"}
        data = {"user_id":"55d4404db217c46ed9ca2b7f","word":"郑州大妈"}
        url = 'http://127.0.0.1:8090/user/search?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'GET'
        request = urllib2.urlopen(request)
        print request.read()
        # self.assertEqual(myclass.sub(2, 1), 1, 'test sub fail')


    def test_post(self):
        # url = 'http://127.0.0.1:8090/user?type=2&id=13800138000&pwd=1111111'
        # values = {'type': '2', "id": "13800138000", "pwd": "11111"}
        user_id = "55d4404db217c46ed9ca2b7f"
        word = u"人民日报"
        data = {"user_id":"55d81cd1b217c414ea07eb9c","word":"郑州大妈街头打人"}
        url = 'http://127.0.0.1:8090/user/search?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'POST'
        request = urllib2.urlopen(request)
        print request.read()
        # self.assertEqual(myclass.sub(2, 1), 1, 'test sub fail')

        # connect('project1', host='mongodb://182.92.78.106:27017/test')

        # user = User.objects(id=user_id).first()

        #print user.user_words

        #word_id = utils.md5(word)
        #word_record = Words.objects(word_id=word_id).first()

        #print word_record.user_count

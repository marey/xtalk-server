# coding=utf-8
__author__ = 'MuRui'

from unittest import TestCase

__author__ = 'MuRui'

import urllib2
from urllib import urlencode
from rong import *
import utils

class TestUserHandler(TestCase):
    def test_userid(self):
        word = u"百度世界大会"
        id = utils.md5(word)
        print id
        chatrooms = {id:word}
        # api_client = ApiClient()
        # response = api_client.chatroom_create(chatrooms)

        print response

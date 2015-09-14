# coding=utf-8
__author__ = 'MuRui'

from unittest import TestCase

__author__ = 'MuRui'

import urllib2
from urllib import urlencode
from rong import *
import utils
from qiniu import Auth,put_file
import json

class TestUserHandler(TestCase):
    def test_userid(self):
        word = u"百度世界大会"
        id = utils.md5(word)
        print id
        chatrooms = {id:word}
        # api_client = ApiClient()
        # response = api_client.chatroom_create(chatrooms)

        # print response

    def test_upload_file_to_qiniu(self):
        data = {"type":"2","id":"13488669692","pwd":"12345678"}
        url = 'http://127.0.0.1:8090/user/login?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'POST'
        request = urllib2.urlopen(request)
        response =  request.read()

        result = json.loads(str(response))

        token = result.get("result").get("qiniu_token")

        mime_type = "image/png"

        localfile = "E:\\murui.png"

        ret, info = put_file(token, "test.png", localfile, mime_type=mime_type, check_crc=True)


        print ret,info


    def test_group_create(self):
        data = {"user_id":"55f05ffdb217c46aad2e68d4","word":"交言"}
        url = 'http://127.0.0.1:8090/group/create?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'GET'
        request = urllib2.urlopen(request)
        response =  request.read()
        print response

    def test_user_group(self):
        data = {"user_id":"55efe49fb217c4686b3558a2"}
        url = 'http://127.0.0.1:8090/user/group?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'GET'
        request = urllib2.urlopen(request)
        response =  request.read()
        print response
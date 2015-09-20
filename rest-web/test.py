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

    def test_user_search(self):
        data = {"user_id":"55f6721cb217c47d78b3f6bf","word":"父亲湿透为儿撑伞"}
        url = 'http://127.0.0.1:8090/user/search?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'POST'
        request = urllib2.urlopen(request)
        response =  request.read()
        print response

    def test_user_search(self):
        data = {"user_id":"55f6721cb217c47d78b3f6bf","group_id":"5929782412a71401aa1a1b60842e97d0"}
        url = 'http://127.0.0.1:8090/group?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'GET'
        request = urllib2.urlopen(request)
        response =  request.read()
        print response

    def test_words_get(self):
        data = {"user_id": "55f6721cb217c47d78b3f6bf", "type": "0"}
        url = 'http://127.0.0.1:8090/words?'

        url = url + urlencode(data)

        # jdata = json.dumps(values)
        request = urllib2.Request(url)
        request.get_method = lambda: 'GET'
        request = urllib2.urlopen(request)
        response = request.read()
        print response

    def test_web_words_add(self):
        word_list = []
        word_list.append("上课")
        word_list.append("上自习")
        word_list.append("吃东西")
        word_list.append("失眠")
        word_list.append("看书")
        word_list.append("乘车")
        word_list.append("洗澡")
        word_list.append("逛街购物")
        word_list.append("旅行")
        word_list.append("拉粑粑")
        word_list.append("遛狗")
        word_list.append("喝咖啡")
        word_list.append("酒吧夜店")
        word_list.append("看球")
        word_list.append("k歌")
        word_list.append("打游戏")
        word_list.append("打台球")
        word_list.append("听歌")
        word_list.append("听电台")
        word_list.append("看电影")
        word_list.append("看美剧")
        word_list.append("看动漫")
        word_list.append("跑步")
        word_list.append("散步")
        word_list.append("健身")
        word_list.append("瑜伽")
        word_list.append("打篮球")
        word_list.append("踢足球")
        word_list.append("游泳")
        word_list.append("玩桌游")
        word_list.append("听讲座")
        word_list.append("骑马")
        word_list.append("飙车")
        word_list.append("钓鱼")
        word_list.append("听音乐会")
        word_list.append("玩音乐节")
        word_list.append("看话剧")
        word_list.append("开会")
        word_list.append("加班")
        word_list.append("堵车")
        word_list.append("滚床单")
        word_list.append("耍孩子")
        word_list.append("看片儿")
        word_list.append("做饭")
        word_list.append("画画")
        word_list.append("写作")
        word_list.append("SPA")
        word_list.append("逛展会")
        word_list.append("遛狗")
        word_list.append("做饭")
        word_list.append("撕逼")
        word_list.append("玩手机")
        word_list.append("创业")
        word_list.append("哭泣")
        word_list.append("生病")
        word_list.append("不开心")
        for word in word_list:
            data = {"word": word, "word_type": "5"}
            url = 'http://127.0.0.1:8090/web/words/add?'

            url = url + urlencode(data)

            # jdata = json.dumps(values)
            request = urllib2.Request(url)
            request.get_method = lambda: 'GET'
            request = urllib2.urlopen(request)
            response = request.read()
            print response

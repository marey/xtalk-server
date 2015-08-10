# coding=utf-8
__author__ = 'MuRui'
import unittest
import urllib2
import time
import json
import os
from rong import *


class mytest(unittest.TestCase):
    ##初始化工作
    def setUp(self):
        pass

        # 退出清理工作

    def tearDown(self):
        pass

    def test_rong_get_token(self):
        api_client = ApiClient()
        api_client.user_get_token("","","")


    def test_os_environ(self):
        print os.environ.get('rongcloud_app_key')


    def test_request_add_method(self):
        url='http://127.0.0.1:8888/test'
        values={'user':'Smith'}

        jdata = json.dumps(values)
        request = urllib2.Request(url, jdata)
        request.add_header('Content-Type', 'your/conntenttype')
        request.get_method = lambda:'add'        # 设置HTTP的访问方式
        request = urllib2.urlopen(request)
        print request.read()

    def test_upload_user_photo(self):
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        data.append('--%s' % boundary)

        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'username')
        data.append('jack')
        data.append('--%s' % boundary)

        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'mobile')
        data.append('13800138000')
        data.append('--%s' % boundary)

        fr = open('D:\\murui.png', 'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename="murui.png"' % 'file')
        data.append('Content-Type: %s\r\n' % 'image/png')
        data.append(fr.read())
        fr.close()
        data.append('--%s--\r\n' % boundary)

        http_url = 'http://localhost:8888/user/upload_photo'
        http_body = '\r\n'.join(data)

        qrcont = None
        try:
            #buld http request
            req = urllib2.Request(http_url, data=http_body)
            #header
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
            req.add_header('User-Agent', 'Mozilla/5.0')
            # req.add_header('Referer', 'http://remotserver.com/')
            #post data to server

            resp = urllib2.urlopen(req, timeout=5)
            #get response
            qrcont = resp.read()
            print qrcont


        except Exception, e:
            print 'http error',e.message


        self.assertEqual(qrcont, None, 'test sub fail')


if __name__ == '__main__':
    unittest.main()
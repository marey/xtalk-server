# coding=utf-8
__author__ = 'MuRui'

import tornado.ioloop
import tornado.web

from handler import *


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # record = db.user_info.inert({'id':1,'name':'kaka','sex':'male'})
        # print record
        self.write("Hello, world")

class TestHandler(tornado.web.RequestHandler):
    def add(self):
        # record = db.user_info.inert({'id':1,'name':'kaka','sex':'male'})
        # print record
        self.write("Hello, world")

class UserUploadPhotoHandler(tornado.web.RequestHandler):
    def post(self):
        print self.request.files
        file_metas=self.request.files['file']   # 提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filename=meta['filename']
            filepath=os.path.join("E:\\",filename)
            with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            self.write('finished!')


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/user", UserHandler),
    (r"/user/black", UserBlackHandler),
    (r"/test", TestHandler),

    (r"/user/upload_photo", UserUploadPhotoHandler),
])

if __name__ == "__main__":
    application.listen(8090)
    tornado.ioloop.IOLoop.instance().start()
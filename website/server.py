# coding=utf-8
__author__ = 'MuRui'

import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "page"),
}

application = tornado.web.Application([
    (r"/", MainHandler),

    # TODO
    # 投诉的意见
    # 聊天成员列表

    # (r"/test", TestHandler),

    # (r"/user/upload_photo", UserUploadPhotoHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

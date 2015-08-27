# coding=utf-8
__author__ = 'MuRui'

import tornado.ioloop
import tornado.web

from handler import *
from web_handler import *


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "page"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/web/login", WebLoginHandler),
    (r"/web/main/left", WebMainLeftHandler),
    (r"/web/main/top", WebMainTopHandler),
    (r"/web/main/index", WebMainIndexHandler),
    (r"/web/words/get", WebWordsGetHandler),



    (r"/user", UserHandler),
    (r"/user/login", UserLoginHandler),
    (r"/user/pwd", UserChangePwdHandler),
    (r"/black", UserBlackHandler),
    (r"/user/other", UserOtherHandler),
    # (r"/user/channel", UserChannelHandler),
    (r"/words", WordsHandler),
    (r"/user/search", UserSearchHandler),
    (r"/user/report", UserReportHandler),
    (r"/os/version", OsVersionHandler),

    (r"/group/create", GroupCreateHandler),
    # (r"/group/join", GroupJoinHandler),
    (r"/group/dismiss", GroupDismissHandler),
    (r"/group/report", GroupReportHandler),
    (r"/group/user/list", GroupUserListHandler),

    # TODO
    # 投诉的意见
    # 聊天成员列表

    # (r"/test", TestHandler),

    # (r"/user/upload_photo", UserUploadPhotoHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8090)
    tornado.ioloop.IOLoop.instance().start()
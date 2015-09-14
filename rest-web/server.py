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
    (r"/web/words/add", WebWordsAddHandler),
    (r"/web/words/search", WebWordSearchHandler),
    (r"/web/words/top_search", WebWordTopSearchHandler),
    (r"/web/words/index", WebWordIndexHandler),
    (r"/web/words/top/add", WebWordAddTopHandler),
    (r"/web/words/top/del", WebWordTopDelHandler),
    (r"/web/user/index", WebUserIndexHandler),
    (r"/web/user/list", WebUserListHandler),
    (r"/web/user/info/index", WebUserInfoIndexHandler),
    (r"/web/user/info/word/get", WebUserInfoWordGetHandler),
    (r"/web/user/info/group/get", WebUserInfoGroupGetHandler),







    (r"/user", UserHandler),
    (r"/user/login", UserLoginHandler),
    (r"/user/pwd", UserChangePwdHandler),
    (r"/black", UserBlackHandler),
    (r"/user/other", UserOtherHandler),
    (r"/user/group", UserGroupHandler),
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
    (r"/sys/setting", SysSettingHandler),

    # TODO
    # 投诉的意见
    # 聊天成员列表

    # (r"/test", TestHandler),

    # (r"/user/upload_photo", UserUploadPhotoHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8090)
    tornado.ioloop.IOLoop.instance().start()
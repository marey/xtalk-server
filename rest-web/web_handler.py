# coding=utf-8

__author__ = 'murui'

from model import *

from handler import BaseHandler
import datetime
import utils


class MainHandler(BaseHandler):
    def get(self):
        self.render("login.html")


class WebMainLeftHandler(BaseHandler):
    def get(self):
        self.render("left.html")


class WebMainTopHandler(BaseHandler):
    def get(self):
        self.render("top.html")


class WebMainIndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class WebLoginHandler(BaseHandler):
    def post(self):
        user_name = self.get_argument("user_name")
        user_pwd = self.get_argument("user_pwd")
        self.render("main.html")


class WebWordsGetHandler(BaseHandler):
    def get(self):
        self.render("right.html")


class WebWordsAddHandler(BaseHandler):
    def get(self):
        word_list = self.get_argument("word", default="").split("\n")
        if len(word_list) > 0:
            for word_item in word_list:
                word = word_item.strip()
                word_id = utils.md5(word)
                record_word = Words.objects(word_id=word_id).first()
                if record_word is not None:
                    self.write("该词条已经存在！")
                else:
                    word_type = int(self.get_argument("word_type", default=1))
                    record_word = Words()

                    record_word.word_id = word_id
                    record_word.word = word
                    record_word.src_type = word_type
                    record_word.word_type = 1
                    record_word.save()

                    top_flg = int(self.get_argument("word_type", default=1))
                    if top_flg == 1:
                        top_word = TopWords()
                        top_word.type = record_word.src_type
                        top_word.word_id = record_word.word_id
                        top_word.word = record_word.word
                        top_word.save()

                    self.write("词条添加成功！")

        self.finish()


class WebWordIndexHandler(BaseHandler):
    def get(self):
        result = []
        words = Words.objects(src_type=1).order_by('-created')[:100]
        for word in words:
            result.append(
                {"id": str(word.id), "word_id": word.word_id, "word": word.word,
                 "created": word.created.strftime('%Y-%m-%d %H:%M:%S')})

        self.render("words/baidu_search_index.html", items=result, key_word="",
                    top_key_word="")


class WebWordAddTopHandler(BaseHandler):
    def get(self):
        param_id = self.get_argument("id")

        result = []
        word = Words.objects(id=param_id).first()

        if word is not None:
            top_word = TopWords.objects(word_id=word.word_id).first()
            if top_word is None:
                top_word = TopWords()
                top_word.type = word.src_type
                top_word.word_id = word.word_id
                top_word.word = word.word
                top_word.save()
            else:
                top_word.created = datetime.datetime.now()
                top_word.save()

            self.write("置顶成功！")
            self.finish()

class WebWordTopDelHandler(BaseHandler):
    def get(self):
        param_id = self.get_argument("id")
        TopWords.objects(id=param_id).delete()
        self.write("删除成功！")
        self.finish()


class WebWordSearchHandler(BaseHandler):
    def get(self):
        key_word = self.get_argument("key_word", default="")
        type = int(self.get_argument("word_type", default=0))

        if type == 0:
            if len(key_word) == 0:
                words = Words.objects().order_by('-created')[:100]
            else:
                words = Words.objects(word__icontains=key_word).order_by('-created')
        else:
            if len(key_word) == 0:
                words = Words.objects(src_type=type).order_by('-created')[:100]
            else:
                words = Words.objects(src_type=type, word__icontains=key_word).order_by('-created')

        data_list = []

        if words is not None and len(words) > 0:
            for word in words:
                data_list.append([word.word_id, word.word.encode("utf8"),
                                  word.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  str(word.id)])

        # self.write({"data": data_list, "draw": 2, "recordsTotal": len(data_list), "recordsFiltered": len(data_list)})
        self.write({"data": data_list})
        self.finish()


class WebWordTopSearchHandler(BaseHandler):
    def get(self):

        key_word = self.get_argument("top_key_word", default="")
        type = int(self.get_argument("top_word_type", default=1))
        result = []
        words = None
        if len(key_word) == 0:
            words = TopWords.objects(type=type).order_by('-created')[:100]
        else:
            words = TopWords.objects(type=type, word__icontains=key_word).order_by('-created')

        data_list = []

        if words is not None and len(words) > 0:
            for word in words:
                down_time = word.created + datetime.timedelta(hours=2)
                data_list.append([word.word_id, word.word.encode("utf8"),
                                  word.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  down_time.strftime('%Y-%m-%d %H:%M:%S'),
                                  str(word.id)])

        self.write({"data": data_list, "draw": 0, "recordsTotal": len(data_list), "recordsFiltered": len(data_list)})

        self.finish()


class WebUserIndexHandler(BaseHandler):
    def get(self):
        self.render("users/user_index.html")

# 用户的列表信息
class WebUserListHandler(BaseHandler):
    def get(self):
        user_id = self.get_argument("user_id", default="")
        user_name = self.get_argument("user_name", default="")
        user_list = None
        if len(user_id) == 0 and len(user_name) == 0:
             user_list = User.objects().order_by('-created')[:100]
        elif len(user_id) != 0:
            user_list = User.objects(id=user_id)
        elif len(user_name) != 0:
            user_list = User.objects(user_name__icontains=user_name).order_by('-created')[:100]
        else:
            user_list = User.objects(id=user_id,user_name__icontains=user_name)

        data_list = []

        if user_list is not None and len(user_list) > 0:
            for user in user_list:
                data_list.append([user.user_photo_url,str(user.id),user.user_telephone, user.user_name,
                                  user.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  str(user.id)])

        self.write({"data": data_list, "draw": 0, "recordsTotal": len(data_list), "recordsFiltered": len(data_list)})

        self.finish()

# 获取用户信息
class WebUserInfoIndexHandler(BaseHandler):
    def get(self):
        user_id = self.get_argument("user_id", default="")
        user = User.objects(id=user_id).first()
        result = {}
        type_list = ["微信注册","微博注册","手机号码注册"]
        sex_list = ["","男","女"]
        result["user_id"] = user_id
        result["authen_type"] = type_list[user.authen_type]
        result["user_name"] = user.user_name
        result["user_photo_url"] = user.user_photo_url
        result["user_sex"] = sex_list[user.user_sex]
        result["user_birthday"] = user.user_birthday
        result["user_region"] = user.user_region
        result["user_sign"] = user.user_sign
        result["user_telephone"] = user.user_telephone
        result["rong_token"] = user.rong_token
        result["created"] = user.created.strftime('%Y-%m-%d %H:%M:%S')

        self.render("users/user_info.html",**result)

# 用户的列表信息
class WebUserInfoWordGetHandler(BaseHandler):
    def get(self):
        user_id = self.get_argument("user_id", default="")

        user = User.objects(id=user_id).order_by('-user_words__created').first()

        data_list = []

        if user is not None and user.user_words is not None and len(user.user_words) > 0:
            for user_word in user.user_words:
                word = Words.objects(id=user_word.word_id).first()

                data_list.append([str(user_word.word_id),user_word.word,
                                  user_word.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  str(word.user_count),
                                  str(len(word.users)),
                                  word.created.strftime('%Y-%m-%d %H:%M:%S')])

        self.write({"data": data_list})
        self.finish()

# 查看用户加入的聊天群组
class WebUserInfoGroupGetHandler(BaseHandler):
    def get(self):
        user_id = self.get_argument("user_id", default="")

        words = Words.objects(users__group_user_id = user_id).order_by('-users__created')

        data_list = []

        if len(words) > 0:
            for user_word in words:
                word = Words.objects(word_id=user_word.word_id).first()

                data_list.append([str(user_word.word_id),user_word.word,
                                  user_word.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  str(word.user_count),
                                    str(len(user_word.users))])

        self.write({"data": data_list})
        self.finish()


class WebServerRequestErrorInfoIndexHandler(BaseHandler):
    def get(self):
        self.render("server/request_error_info.html")

class WebServerRequestErrorInfoSearchHandler(BaseHandler):
    def get(self):
        uri = self.get_argument("uri", default="")

        if len(uri) == 0:
            error_info_list = SysError.objects().order_by('-created')
        else:
            error_info_list = SysError.objects(uri__icontains = uri).order_by('-created')

        data_list = []

        if len(error_info_list) > 0:
            for error_info in error_info_list:

                data_list.append([error_info.method_name,error_info.uri,error_info.error_info,
                                  error_info.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  ])

        self.write({"data": data_list})
        self.finish()
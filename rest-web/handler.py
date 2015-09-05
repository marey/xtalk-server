# coding=utf-8

__author__ = 'murui'

import tornado.web
from bson.objectid import ObjectId

from message import MessageUtils
from model import *
import utils
from rong import *


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        connect('project1', host='mongodb://182.92.78.106:27017/test')
        self._response = {"code": "200", "message": "", "result": ""}
        self._result = None

    def check_params_exists(self, key):
        """
            判断参数是否存在
        :param key:需要判断的参数
        """
        value = self.get_argument(key, default=None)

        # 判断是否为空
        if value is None or len(value) == 0:
            raise tornado.web.HTTPError("40001", MessageUtils.ERROR_0001, key)
        if cmp("user_id", key) == 0:
            self.check_user_id(value)

    # 验证有效性
    def check_user_id(self, user_id):

        if ObjectId.is_valid(user_id) is False:
            raise tornado.web.HTTPError("40002", MessageUtils.ERROR_0002, user_id)

    def on_write(self):
        if self._result is not None:
            self._response["result"] = self._result
        # self.set_header("Content-Type", "application/json")
        self.write(self._response)

    def write_error(self, status_code, exception=None, **kwargs):
        if status_code == 500:
            response_result = {"code": "40015"}
            exec_info = kwargs.get("exc_info", None)
            if exec_info is not None and len(exec_info) == 3:
                response_result["message"] = MessageUtils.ERROR_0015.format(exec_info[1])

            self.write(response_result)


class UserLoginHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        """
            实际上是做user的login操作
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("type")
            self.check_params_exists("id")
            self.check_params_exists("pwd")
            # 获取登陆用户的信息
            self.login_user()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def login_user(self):
        type = int(self.get_argument("type"))
        param_id = self.get_argument("id")
        if type == 2:
            # user_pwd = utils.md5(self.get_argument("pwd", default=None))
            user_pwd = self.get_argument("pwd")
            login_id = utils.md5(param_id)
            user = User.objects(authen_type=type, login_id=login_id).first()
            if user is None:
                raise tornado.web.HTTPError("40010", MessageUtils.ERROR_0010)
            elif cmp(user_pwd, user.user_pwd) != 0:
                raise tornado.web.HTTPError("40003", MessageUtils.ERROR_0003)
            result = {}
            result["user_id"] = str(user.id)
            result["name"] = user.user_name
            result["photo"] = user.user_photo_url
            result["sex"] = user.user_sex
            result["region"] = user.user_region
            result["signature"] = user.user_sign
            result["phone"] = user.user_telephone
            result["token"] = user.rong_token
            # user_words = user.user_words
            # if user_words is not None:
            # word_list = []
            # for word in user_words[:6]:
            # word_list.append(word.word)
            #
            # reslut["user_words"] = word_list

            self._result = result


# 用户修改密码
class UserChangePwdHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        """
            用户修改密码
        :return: 处理后的json的数组
        """
        try:
            # 检查参数的传入
            self.check_params_exists("phone")
            self.check_params_exists("pwd")
            # 获取登陆用户的信息
            self.change_user_pwd()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def change_user_pwd(self):
        phone = self.get_argument("phone")
        login_id = utils.md5(phone)
        user = User.objects(authen_type=2, login_id=login_id).first()
        if user is None:
            raise tornado.web.HTTPError("40009", MessageUtils.ERROR_0009, phone)
        else:
            # user.user_pwd = utils.md5(self.get_argument("pwd"))
            user.user_pwd = self.get_argument("pwd")
            user.save()


# 用户登录处理
class UserHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
            用户信息的获取
        :return:
        """
        try:
            # 检查参数的传入
            self.check_get_params()
            # 获取用户信息
            self.get_user_info()
        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        """
            注册用户
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_post_params()
            # 获取登陆用户的信息
            self.register_user()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def put(self):
        """
            编辑user的内容，编辑用户的信息
        :return: 返回处理后的json字符串
        """
        try:
            # 检查参数的传入
            # 判断参数是否存在
            self.check_params_exists("user_id")
            self.check_params_exists("name")
            self.check_params_exists("photo")
            self.check_params_exists("region")
            self.check_params_exists("signature")
            self.check_params_exists("sex")
            # 获取登陆用户的信息
            self.edit_user_info()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def edit_user_info(self):
        user_id = self.get_argument("user_id")
        user_name = self.get_argument("name")
        user_photo_url = self.get_argument("photo")
        user_region = self.get_argument("region")
        user_sign = self.get_argument("signature")
        user_sex = self.get_argument("sex", 1)
        if user_sex in [1, 2]:
            raise tornado.web.HTTPError("40002", MessageUtils.ERROR_0002, user_sex)

        User.objects(id=user_id).update_one(set__user_name=user_name, set__user_sex=user_sex,
                                            set__user_photo_url=user_photo_url, set__user_region=user_region,
                                            set__user_sign=user_sign)

    def check_get_params(self):
        # 判断参数是否存在
        self.check_params_exists("user_id")

    def get_user_info(self):
        user_id = self.get_argument("user_id", default=None)
        user = User.objects(id=user_id).first()

        if user is not None:
            result = {}
            result["name"] = user.user_name
            result["photo"] = user.user_photo_url
            result["sex"] = user.user_sex
            result["region"] = user.user_region
            result["signature"] = user.user_sign
            result["phone"] = user.user_telephone
            user_words = user.user_words
            if user_words is not None:
                word_list = []
                for word in user_words[:6]:
                    word_list.append(word.word)

                result["user_words"] = word_list

            self._result = result

    def register_user(self):

        # 0,表示微信，1，表示微博，2，表示手机号
        type = int(self.get_argument("type", default=0))
        param_id = self.get_argument("id", default=None)
        param_name = self.get_argument("name", default="")
        user_photo_url = self.get_argument("photo", default="")

        if type != 2:
            # user = User.objects(authen_type=type,login_id=login_id).first()
            raise tornado.web.HTTPError("40002", MessageUtils.ERROR_0002, "type")

        # pwd = utils.md5(self.get_argument("pwd", default=None))
        pwd = self.get_argument("pwd")
        login_id = utils.md5(param_id)
        user = User.objects(authen_type=type,
                            login_id=login_id,
                            user_pwd=pwd).first()

        if user is not None:
            raise tornado.web.HTTPError("40006", MessageUtils.ERROR_0006, login_id)

        api_client = ApiClient()
        response = api_client.user_get_token(login_id, param_name, user_photo_url)

        code = response.get("code", None)
        if code is not None and code == 200:
            token = response.get("token")
        else:
            raise tornado.web.HTTPError("40003", MessageUtils.ERROR_0003)

        if user is None:
            # 将数据保存到数据库中
            user = User()
            user.authen_type = type
            user.login_id = login_id
            user.user_name = self.get_argument("name", default=None)
            # user.user_pwd = utils.md5(self.get_argument("pwd", default=None))
            user.user_pwd = self.get_argument("pwd")
            user.user_photo_url = self.get_argument("photo", default=None)
            user.user_sex = self.get_argument("sex", default=None)
            user.user_region = self.get_argument("region", default=None)
            user.rong_token = token
            user.user_telephone = param_id
            user.save()

        self._result = {"user_id": str(user.pk), "token": token}

    def check_post_params(self):

        type = self.get_argument("type", default=None)

        # 判断是否为空
        if type is None:
            raise tornado.web.HTTPError("40001", MessageUtils.ERROR_0001, "type")
        # 判断是否在可控的范围内
        if type not in ["0", "1", "2"]:
            raise tornado.web.HTTPError("40002", MessageUtils.ERROR_0002, "type")

        id = self.get_argument("id", default=None)
        if id is None:
            raise tornado.web.HTTPError("40001", MessageUtils.ERROR_0001, "id")

        pwd = self.get_argument("pwd", default=None)

        if cmp(type, "2") == 0:
            if pwd is None:
                raise tornado.web.HTTPError("40001", MessageUtils.ERROR_0001, "pwd")
            elif len(pwd) < 6:
                raise tornado.web.HTTPError("40008", MessageUtils.ERROR_0008)

            phone_number = utils.check_mobile_phone(id)
            if phone_number is None:
                raise tornado.web.HTTPError("40007", MessageUtils.ERROR_0007)

        name = self.get_argument("name", default=None)
        if name is None:
            raise tornado.web.HTTPError("40001", MessageUtils.ERROR_0001, "name")

        photo = self.get_argument("photo", default=None)
        if photo is None:
            raise tornado.web.HTTPError("40001", MessageUtils.ERROR_0001, "photo")


# 用户推荐频道
class UserChannelHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
            用户推荐频道的添加
        :return:
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("channel_name")
            self.add_user_channel()

        except tornado.web.HTTPError, e:
            code = e.status_code
            message = e.log_message.format(e.args)

        # 将数据整理后返回
        response = {}

        response["code"] = code
        response["message"] = message
        response["result"] = result

        self.write(json.dumps(response))
        self.finish()

    def add_user_channel(self):
        user_id = self.get_argument("user_id")
        channel_name = self.get_argument("channel_name").trim()
        user_channel = UserChannel(id=hash(channel_name), channel_name=channel_name).save()
        User.objects(id=user_id).update_one(push__authors=user_channel)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
            用户推荐频道的添加
        :return:
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            result = self.get_user_channel()

        except tornado.web.HTTPError, e:
            code = e.status_code
            message = e.log_message.format(e.args)

        # 将数据整理后返回
        response = {}

        response["code"] = code
        response["message"] = message
        response["result"] = result

        self.write(json.dumps(response))
        self.finish()

    def get_user_channel(self):
        user_id = self.get_argument("user_id")

        channels = SysChannel.objects.order_by("+order_by", "+tags__order_by")

        result = {}

        return result


# 用户登录处理
class UserSearchHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
            实时查询，匹配用户的查询词
        :return:
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.user_words_history()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def user_words_history(self):
        user_id = self.get_argument("user_id")
        user = User.objects(id=user_id).first()
        if user is not None and user.user_words is not None and len(user.user_words) > 0:
            user_words = user.user_words[:30]
            word_list = []
            for user_word in user_words:
                word_list.append(user_word.word)

            self._result = word_list

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def delete(self):
        """
            实时查询，匹配用户的查询词
        :return:
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("word")
            self.delete_word()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def delete_word(self):
        user_id = self.get_argument("user_id")
        word = self.get_argument("word")

        user = User.objects(id=user_id).first()
        record_word = Words.objects(word_id=utils.md5(word)).first()
        if record_word is not None and user is not None:
            User.objects(id=user_id).update_one(pull__user_words__word_id=record_word.id)


    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def put(self):
        """
            实时查询，匹配用户的查询词
        :return:
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            # 检查参数的传入
            self.check_params_exists("word")
            self.put_word_search()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def put_word_search(self):
        p_word = self.get_argument("word")
        # p_word = p_word.encode("utf8")
        words = Words.objects(word__icontains=p_word).order_by('-created')[:5]
        map_list = []
        if words is not None:
            # print len(words)
            for word in words:
                map_list.append(word.word)

        if len(map_list) > 0:
            self._result = map_list

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
            用户提交检索的词以后，保存数据
        :return:
        """
        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            # 检查参数的传入
            self.check_params_exists("word")
            # 保存需要查询的词
            self.save_search_word()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)
        self.on_write()
        self.finish()

    def save_search_word(self):
        user_id = self.get_argument("user_id")
        p_word = self.get_argument("word")
        word_id = utils.md5(p_word)
        word = Words.objects(word_id=word_id).first()
        if word is None:
            word = Words()
            word.word_id = word_id
            word.word = p_word
            word.src_type = 0
            word.word_type = None
            word.user_count = 1

            word.save()
        else:
            word.update(inc__user_count=1)

        user_word = UserWords()
        user_word.word_id = word.word_id
        user_word.word = word.word
        # 先删后插
        User.objects(id=user_id).update_one(pull__user_words__word_id=word.word_id)
        User.objects(id=user_id).update_one(push__user_words=user_word)


class WordsHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
            获取首页卡片的词汇内容
        :return:
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("type")
            result = self.get_words()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def get_words(self):
        user_id = self.get_argument("user_id")
        type = int(self.get_argument("type"))

        result = []
        if type == 0:
            # 1 新闻热点
            words = self.get_baidu_words()
            if words is not None:
                result.append(words)
            # 2 影视综艺
            words = self.get_film_words()
            if words is not None:
                result.append(words)
            # 3 热门词条
            words = self.get_top_count_words()
            if words is not None:
                result.append(words)
            # 4 新创词条
            words = self.get_new_created_words()
            if words is not None:
                result.append(words)
            # 5 状态标签
            words = self.get_status_words()
            if words is not None:
                result.append(words)

            # 6 我的词条
            words = self.get_my_words()
            if words is not None:
                result.append(words)

        elif type == 1:
            # 1 新闻热点
            words = self.get_baidu_words()
            if words is not None:
                result.append(words)
        elif type == 2:
            # 0 影视综艺
            words = self.get_film_words()
            if words is not None:
                result.append(words)
        elif type == 3:
            # 0 热门词条
            words = self.get_top_count_words()
            if words is not None:
                result.append(words)
        elif type == 4:
            # 0 新创词条
            words = self.get_new_created_words()
            if words is not None:
                result.append(words)
        elif type == 5:
            # 0 状态标签
            words = self.get_status_words()
            if words is not None:
                result.append(words)
        elif type == 6:
            # 0 状态标签
            words = self.get_my_words()
            if words is not None:
                result.append(words)

        if len(result) > 0:
            self._result = result

    def get_baidu_words(self):
        index = int(self.get_argument("page_index", 0))
        start_index = index * 30
        top_words_count = TopWords.objects(type=1).count()
        words = None
        if top_words_count == 0:
            words = Words.objects(src_type=1).order_by("+created")[index * 30:(index + 1) * 30]
            if len(words) == 0:
                words = Words.objects(src_type=1).order_by("+created")[0:30]
        else:
            if top_words_count >= (index + 1) * 30:
                words = TopWords.objects(type=1).order_by("+created")[index * 30:(index + 1) * 30]
            elif top_words_count < start_index:
                words = Words.objects(src_type=1).order_by("+created")[start_index:(index + 1) * 30]
                if len(words) == 0:
                    words = Words.objects(src_type=1).order_by("+created")[0:30]
            else:
                words = TopWords.objects(type=1).order_by("+created")[start_index:top_words_count]
                word_list = []
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                words = Words.objects(src_type=1).order_by("+created")[0:(index + 1) * 30 - top_words_count]
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                return word_list

        if words is None or len(words) == 0:
            return None

        result = {"type": 1, "type_name": "新闻热点"}
        word_list = []

        for word in words:
            word_map = {}
            if word.word_type == 1:
                word_map["type"] = "新"
            word_map["word_id"] = str(word.word_id)
            word_map["word"] = word.word

            word_list.append(word_map)

        result["words"] = word_list

        return result


    def get_film_words(self):
        result = {"type": 2, "type_name": "影视综艺"}
        index = int(self.get_argument("page_index", 0))
        start_index = index * 30
        top_words_count = TopWords.objects(type=2).count()
        words = None
        if top_words_count == 0:
            words = Words.objects(src_type=2).order_by("+created")[index * 30:(index + 1) * 30]
            if len(words) == 0:
                words = Words.objects(src_type=2).order_by("+created")[0:30]
        else:
            if top_words_count >= (index + 1) * 30:
                words = TopWords.objects(type=2).order_by("+created")[index * 30:(index + 1) * 30]
            elif top_words_count < start_index:
                words = Words.objects(src_type=2).order_by("+created")[start_index:(index + 1) * 30]
                if len(words) == 0:
                    words = Words.objects(src_type=2).order_by("+created")[0:30]
            else:
                words = TopWords.objects(type=2).order_by("+created")[start_index:top_words_count]
                word_list = []
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                words = Words.objects(src_type=2).order_by("+created")[0:(index + 1) * 30 - top_words_count]
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                result["words"] = word_list
                return result

        if words is None or len(words) == 0:
            return None

        word_list = []

        for word in words:
            word_map = {}
            if word.word_type == 1:
                word_map["type"] = "新"
            word_map["word_id"] = str(word.word_id)
            word_map["word"] = word.word

            word_list.append(word_map)

        result["words"] = word_list

        return result

    def get_top_count_words(self):

        result = {"type": 3, "type_name": "热门词条"}
        index = int(self.get_argument("page_index", 0))
        start_index = index * 30
        top_words_count = TopWords.objects(type=3).count()
        words = None
        if top_words_count == 0:
            words = Words.objects().order_by("-user_count")[index * 30:(index + 1) * 30]
            if len(words) == 0:
                words = Words.objects().order_by("-user_count")[0:30]
        else:
            if top_words_count >= (index + 1) * 30:
                words = TopWords.objects(type=3).order_by("+created")[index * 30:(index + 1) * 30]
            elif top_words_count < start_index:
                words = Words.objects().order_by("-user_count")[index * 30:(index + 1) * 30]
                if len(words) == 0:
                    words = Words.objects().order_by("-user_count")[0:30]
            else:
                words = TopWords.objects(type=3).order_by("+created")[start_index:top_words_count]
                word_list = []
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                words = Words.objects(src_type=4).order_by("-user_count")[0:(index + 1) * 30 - top_words_count]
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                result["words"] = word_list
                return result

        if words is None or len(words) == 0:
            return None

        word_list = []

        for word in words:
            word_map = {}
            if word.word_type == 1:
                word_map["type"] = "新"
            word_map["word_id"] = str(word.word_id)
            word_map["word"] = word.word

            word_list.append(word_map)

        result["words"] = word_list

        return result


    def get_new_created_words(self):
        result = {"type": 4, "type_name": "新创词条"}
        index = int(self.get_argument("page_index", 0))
        start_index = index * 30
        top_words_count = TopWords.objects(type=4).count()
        words = None
        if top_words_count == 0:
            words = Words.objects(src_type=4).order_by("+created")[index * 30:(index + 1) * 30]
            if len(words) == 0:
                words = Words.objects(src_type=4).order_by("+created")[0:30]
        else:
            if top_words_count >= (index + 1) * 30:
                words = TopWords.objects(type=4).order_by("+created")[index * 30:(index + 1) * 30]
            elif top_words_count < start_index:
                words = Words.objects(src_type=4).order_by("+created")[start_index:(index + 1) * 30]
                if len(words) == 0:
                    words = Words.objects(src_type=4).order_by("+created")[0:30]
            else:
                words = TopWords.objects(type=4).order_by("+created")[start_index:top_words_count]
                word_list = []
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                words = Words.objects(src_type=4).order_by("+created")[0:(index + 1) * 30 - top_words_count]
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                result["words"] = word_list
                return result

        if words is None or len(words) == 0:
            return None

        word_list = []

        for word in words:
            word_map = {}
            if word.word_type == 1:
                word_map["type"] = "新"
            word_map["word_id"] = str(word.word_id)
            word_map["word"] = word.word

            word_list.append(word_map)

        result["words"] = word_list

        return result

    def get_status_words(self):
        result = {"type": 5, "type_name": "状态标签"}
        index = int(self.get_argument("page_index", 0))
        start_index = index * 30
        top_words_count = TopWords.objects(type=5).count()
        words = None
        if top_words_count == 0:
            words = Words.objects(src_type=5).order_by("+created")[index * 30:(index + 1) * 30]
            if len(words) == 0:
                words = Words.objects(src_type=5).order_by("+created")[0:30]
        else:
            if top_words_count >= (index + 1) * 30:
                words = TopWords.objects(type=5).order_by("+created")[index * 30:(index + 1) * 30]
            elif top_words_count < start_index:
                words = Words.objects(src_type=5).order_by("+created")[start_index:(index + 1) * 30]
                if len(words) == 0:
                    words = Words.objects(src_type=5).order_by("+created")[0:30]
            else:
                words = TopWords.objects(type=5).order_by("+created")[start_index:top_words_count]
                word_list = []
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                words = Words.objects(src_type=5).order_by("+created")[0:(index + 1) * 30 - top_words_count]
                for word in words:
                    word_map = {}
                    if word.word_type == 1:
                        word_map["type"] = "新"
                    word_map["word_id"] = str(word.word_id)
                    word_map["word"] = word.word

                    word_list.append(word_map)

                result["words"] = word_list
                return result

        if words is None or len(words) == 0:
            return None

        word_list = []

        for word in words:
            word_map = {}
            if word.word_type == 1:
                word_map["type"] = "新"
            word_map["word_id"] = str(word.word_id)
            word_map["word"] = word.word

            word_list.append(word_map)

        result["words"] = word_list

        return result

    def get_my_words(self):
        index = int(self.get_argument("page_index", 0))
        user_id = self.get_argument("user_id")
        user = User.objects(id=user_id).first()
        if user is None:
            raise tornado.web.HTTPError("40004", MessageUtils.ERROR_0004, user_id)
        user_words = user.user_words
        if user_words is None or len(user_words) == 0:
            return None
        if len(user_words) > index * 30:
            user_words = user_words[index * 30:(index + 1) * 30]
        else:
            user_words = user_words[:30]

        if len(user_words) == 0:
            return None

        result = {"type": 6, "type_name": "我的词条"}
        word_list = []

        for word in user_words:
            word_map = {}
            word_map["word_id"] = str(word.word_id)
            word_map["word"] = word.word
            word_list.append(word_map)

        result["words"] = word_list

        return result


# 用户的黑名单数据
class UserBlackHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
            用户黑名单的获取
        :return:
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            result = self.get_black_users()

        except tornado.web.HTTPError, e:
            code = e.status_code
            message = e.log_message.format(e.args)

        # 将数据整理后返回
        response = {}

        response["code"] = code
        response["message"] = message
        response["result"] = result

        self.write(json.dumps(response))
        self.finish()

    def get_black_users(self):

        user_id = self.get_argument("user_id")
        user = User.objects(id=user_id).only("black_users").first()
        map_list = []
        if user is not None and user.black_users is not None:

            for blackUser in user.black_users:
                user_info = User.objects(id=blackUser.user_id).only("user_name", "user_photo_url").first()
                if user_info is not None:
                    user_map = {"user_id": blackUser.user_id, "name": user_info.user_name,
                                "photo": user_info.user_photo_url}
                    map_list.append(user_map)

        if len(map_list) > 0:
            return map_list
        else:
            return ""

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def put(self):
        """
            用户黑名单的添加
        :return:
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("black_user_id")
            self.add_black_user()

        except tornado.web.HTTPError, e:
            code = e.status_code
            message = e.log_message.format(e.args)

        # 将数据整理后返回
        response = {}

        response["code"] = code
        response["message"] = message
        response["result"] = result

        self.write(json.dumps(response))
        self.finish()

    def add_black_user(self):
        user_id = self.get_argument("user_id")
        black_user_id = self.get_argument("black_user_id")
        black_user = BlackUser(user_id=black_user_id)

        # 先删后插
        User.objects(id=user_id).update_one(pull__black_users__user_id=black_user_id)
        User.objects(id=user_id).update_one(push__black_users=black_user)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def delete(self):
        """
            用户黑名单的删除
        :return:
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("black_user_id")
            self.del_black_user()

        except tornado.web.HTTPError, e:
            code = e.status_code
            message = e.log_message.format(e.args)

        # 将数据整理后返回
        response = {}

        response["code"] = code
        response["message"] = message
        response["result"] = result

        self.write(json.dumps(response))
        self.finish()

    def del_black_user(self):
        user_id = self.get_argument("user_id")
        black_user_id = self.get_argument("black_user_id")
        User.objects(id=user_id).update_one(pull__black_users__user_id=black_user_id)


class UserOtherHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        """
            获取我想要查看的人的黑名单列表
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("other_user_id")
            # 保存举报用户的信息
            self.get_other_black()


        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def get_other_black(self):
        user_id = self.get_argument("user_id")
        other_user_id = self.get_argument("other_user_id")

        result = {}

        user = User.objects(id=user_id).first()
        if user is None:
            raise tornado.web.HTTPError("40004", MessageUtils.ERROR_0004, user_id)

        other_user = User.objects(id=other_user_id).first()
        if other_user is None:
            raise tornado.web.HTTPError("40004", MessageUtils.ERROR_0004, user_id)

        result["name"] = user.user_name
        result["photo"] = user.user_photo_url
        result["sex"] = user.user_sex
        result["region"] = user.user_region
        result["signature"] = user.user_sign
        result["phone"] = user.user_telephone
        user_words = user.user_words
        if user_words is not None:
            word_list = []
            for word in user_words[:6]:
                word_list.append(word.word)

            result["user_words"] = word_list

        user = User.objects(id=user_id, black_users__user_id=other_user_id).first()

        other_user = User.objects(id=other_user_id, black_users__user_id=user_id).first()

        if user is not None and other_user is not None:
            result["black_type"] = 3
        elif user is not None:
            result["black_type"] = 1
        elif other_user is not None:
            result["black_type"] = 2
        else:
            result["black_type"] = 0

        self._result = result


class UserReportHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        """
            保存举报的用户信息
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("report_user_id")
            self.check_params_exists("type")
            # 保存举报用户的信息
            self.save_report_user()


        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def save_report_user(self):
        report_user = ReportUser()
        report_user.report_user_id = self.get_argument("report_user_id")
        report_user.user_id = self.get_argument("user_id")
        report_user.type = int(self.get_argument("type"))

        report_user.save()


class OsVersionHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        """
            获取客户端的版本信息
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("os_type")
            # 获取当前的客户端的版本
            self.get_os_version()


        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def get_os_version(self):
        os_type = int(self.get_argument("os_type"))
        version = OsVersion.objects(os_type=os_type).order_by("+created").first()
        if version is not None:
            self._result = {"version": version.version}


class GroupCreateHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        """
            获取客户端的版本信息
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("word")
            # 获取当前的客户端的版本
            self.create_group()


        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def create_group(self):
        user_id = self.get_argument("user_id")
        p_word = self.get_argument("word")
        word_id = utils.md5(p_word)
        word = Words.objects(word_id=word_id).first()

        if word is not None:
            if word.user_group is None:
                self.rong_create_group(user_id, word_id, p_word)

                word_group = WordGroup()
                word_group.group_user_id = user_id
                word.update(set__user_group=word_group)

            word.update(inc__user_count=1)
        else:
            word = Words()
            word.word_id = word_id
            word.word = p_word
            word.src_type = 0
            word.word_type = None
            word.user_count = 1
            self.rong_create_group(user_id, word_id, p_word)

            word_group = WordGroup()
            word_group.group_user_id = user_id
            word.user_group = word_group
            word.save()

        user_word = UserWords()
        user_word.word_id = word.id
        user_word.word = word.word
        # 先删后插
        User.objects(id=user_id).update_one(pull__user_words__word_id=word.id)
        User.objects(id=user_id).update_one(push__user_words=user_word)

        # 加入聊天群组
        self.rong_join_group(user_id, word_id, p_word)

        # 聊天室的列表
        group_user = GroupUsers.objects(word_id=word_id).first()
        if group_user is None:
            group_user = GroupUsers()
            group_user.word_id = word_id
            # 先保存数据
            group_user.save()
            word_group = WordGroup()
            word_group.group_user_id = user_id
            # 然后更新列表
            group_user.update(push__users=word_group)

        self._result = {"group_id": word.id, "group_name": word.word}


    def rong_create_group(self, user_id, word_id, p_word):
        api_client = ApiClient()
        response = api_client.group_create(user_id, word_id, p_word)

        code = response.get("code", None)
        if code is None and code != 200:
            raise tornado.web.HTTPError("40011", MessageUtils.ERROR_0011)

    def rong_join_group(self, user_id, word_id, p_word):
        api_client = ApiClient()
        response = api_client.group_join(user_id, word_id, p_word)

        code = response.get("code", None)
        if code is None and code != 200:
            raise tornado.web.HTTPError("40013", MessageUtils.ERROR_0013)


# 加入群组
class GroupJoinHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        """
            获取客户端的版本信息
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("word")
            # 加入聊天群组
            self.join_group()


        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()


# 销毁群组
class GroupDismissHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        """
            获取客户端的版本信息
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("word")
            # 获取当前的客户端的版本
            self.dismiss_group()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def dismiss_group(self):
        user_id = self.get_argument("user_id")
        p_word = self.get_argument("word")
        word_id = utils.md5(p_word)
        word = Words.objects(word_id=word_id).first()
        if word is not None:
            api_client = ApiClient()
            response = api_client.group_dismiss(user_id, word_id)
            code = response.get("code", None)
            if code is None and code != 200:
                raise tornado.web.HTTPError("40012", MessageUtils.ERROR_0012)

            word.update(set__user_group=None)


# 举报聊天室内的成员
class GroupReportHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        """
            获取客户端的版本信息
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("report_user_id")
            self.check_params_exists("type")
            self.check_params_exists("group_id")
            # 获取当前的客户端的版本
            self.dismiss_group()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def report_group_user(self):
        user_id = self.get_argument("user_id")
        type = self.get_argument("type")
        report_user_id = self.get_argument("report_user_id")
        group_id = self.get_argument("group_id")
        report_user = ReportUser()
        report_user.report_user_id = report_user_id
        report_user.user_id = user_id
        report_user.type = type
        report_user.group_id = group_id
        report_user.save()

        # 判断是否大于3次举报
        count = ReportUser.objects(group_id=group_id, report_user_id=report_user_id).count()
        if count > 3:
            GroupUsers.objects(word_id=group_id).update_one(pull__users__group_user_id=report_user_id)

            api_client = ApiClient()
            response = api_client.group_quit(report_user_id, group_id)
            code = response.get("code", None)
            if code is None and code != 200:
                raise tornado.web.HTTPError("40014", MessageUtils.ERROR_0014)


class GroupUserListHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        """
            获取聊天室内的用户列表
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            self.check_params_exists("group_id")
            # 获取当前的客户端的版本
            self.get_group_user_list()

        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    def get_group_user_list(self):
        user_id = self.get_argument("user_id")
        group_id = self.get_argument("group_id")
        page_index = int(self.get_argument("user_id", 0))

        group_user = GroupUsers.objects(word_id=group_id).first()

        if group_user is not None and len(group_user.users) > 0:
            user_list = []
            for word_group in group_user.users[page_index * 20:page_index * 20 + 20]:
                user = User.objects(id=word_group.group_user_id).first()
                if user is not None:
                    user_list.append({"user_id": str(user.id), "name": user.user_name, "photo": user.user_photo_url})

            if len(user_list) > 0:
                self._result = user_list

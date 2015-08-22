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
        if value is None:
            raise tornado.web.HTTPError("40001", MessageUtils.ERROR_0001, key)
            # if cmp("user_id", key) == 0:
            # self.check_user_id(key)

    # 验证有效性
    def check_user_id(self, user_id):
        try:
            value = ObjectId(user_id)
            # 判断是否为空
        except:
            raise tornado.web.HTTPError("40005", MessageUtils.ERROR_0005, user_id)

    def on_write(self):
        if self._result is not None:
            self._response["result"] = self._result
        # self.set_header("Content-Type", "application/json")
        self.write(self._response)


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
        id = self.get_argument("id")
        if type == 2:
            # user_pwd = utils.md5(self.get_argument("pwd", default=None))
            user_pwd = self.get_argument("pwd")
            user = User.objects(authen_type=type, login_id=id).first()
            if user is None:
                raise tornado.web.HTTPError("40010", MessageUtils.ERROR_0010)
            elif cmp(user_pwd, user.user_pwd) != 0:
                raise tornado.web.HTTPError("40003", MessageUtils.ERROR_0003)
            reslut = {}
            reslut["user_id"] = str(user.id)
            reslut["name"] = user.user_name
            reslut["photo"] = user.user_photo_url
            reslut["sex"] = user.user_sex
            reslut["region"] = user.user_region
            reslut["signature"] = user.user_sign
            reslut["phone"] = user.user_telephone
            # user_words = user.user_words
            # if user_words is not None:
            # word_list = []
            #     for word in user_words[:6]:
            #         word_list.append(word.word)
            #
            #     reslut["user_words"] = word_list

            self._result = reslut


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

        user = User.objects(authen_type=2, login_id=phone).first()
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
            self._result = self.get_user_info()
        except tornado.web.HTTPError, e:
            self._response["code"] = e.status_code
            self._response["message"] = e.log_message.format(e.args)

        self.on_write()
        self.finish()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        """
            实际上是做user的login操作
        :return: 处理后的json的数组
        """

        try:
            # 检查参数的传入
            self.check_post_params()
            # 获取登陆用户的信息
            self._result = self.register_user()

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
        user_telephone = self.get_argument("phone")
        user_sex = self.get_argument("sex")

        User.objects(id=user_id).update_one(set__user_name=user_name, set__user_sex=user_sex,
                                            set__user_photo_url=user_photo_url, set__user_region=user_region,
                                            set__user_sign=user_sign, set__user_telephone=user_telephone)

    def check_get_params(self):
        # 判断参数是否存在
        self.check_params_exists("user_id")

    def get_user_info(self):
        user_id = self.get_argument("user_id", default=None)
        user = User.objects(id=user_id).only("user_name", "user_photo_url", "user_sex", "user_region", "user_sign",
                                             "user_telephone,user_words").first()
        # post = Post.objects.no_dereference().first()
        if user is not None:
            reslut = {}
            reslut["name"] = user.user_name
            reslut["photo"] = user.user_photo_url
            reslut["sex"] = user.user_sex
            reslut["region"] = user.user_region
            reslut["signature"] = user.user_sign
            reslut["phone"] = user.user_telephone
            user_words = user.user_words
            if user_words is not None:
                word_list = []
                for word in user_words[:6]:
                    word_list.append(word.word)

                reslut["user_words"] = word_list

            return reslut

        return ""

    def register_user(self):

        # 0,表示微信，1，表示微博，2，表示手机号
        type = int(self.get_argument("type", default=None))
        login_id = self.get_argument("id", default=None)

        user = None
        if type == 2:
            # pwd = utils.md5(self.get_argument("pwd", default=None))
            pwd = self.get_argument("pwd")
            user = User.objects(authen_type=type,
                                login_id=login_id,
                                user_pwd=pwd).first()

            if user is not None:
                raise tornado.web.HTTPError("40006", MessageUtils.ERROR_0006, login_id)
        else:
            # user = User.objects(authen_type=type,login_id=login_id).first()

            raise tornado.web.HTTPError("40002", MessageUtils.ERROR_0002, "type")

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
            user.save()

        api_client = ApiClient()
        response = api_client.user_get_token(user.pk, user.user_name, user.user_photo_url)

        code = response.get("code", None)
        if code is not None and code == 200:
            token = response.get("token")
        else:
            raise tornado.web.HTTPError("40003", MessageUtils.ERROR_0003)

        reslut = {}
        reslut["user_id"] = str(user.pk)
        reslut["token"] = token
        return reslut

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
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            # 检查参数的传入
            self.check_params_exists("word")
            result = self.get_word_search()

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

    def get_word_search(self):
        p_word = self.get_argument("word")
        # p_word = p_word.encode("utf8")
        words = Words.objects(word__icontains=p_word).order_by('-created')[:5]
        map_list = []
        if words is not None:
            # print len(words)
            for word in words:
                map_list.append(word.word)

        if len(map_list) > 0:
            return map_list
        else:
            return ""

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
            用户提交检索的词以后，保存数据
        :return:
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_params_exists("user_id")
            # 检查参数的传入
            self.check_params_exists("word")
            result = self.get_word_search()
            # 保存需要查询的词
            self.save_search_word()

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

    def save_search_word(self):
        user_id = self.get_argument("user_id")
        p_word = self.get_argument("word")
        word_id = utils.md5(p_word)
        word = Words.objects(word_id=word_id).first()
        if word is None:
            word = Words()
            word.word_id = word_id
            word.word = p_word
            word.src_type = 2
            word.word_type = None
            word.user_count = 1

            word.save()
        else:
            word.update(inc__user_count=1)

        user_word = UserWords()
        user_word.word_id = word.id

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
            # 0 表示获取所有的聊天的词汇
            words = self.get_baidu_words()
            if words is not None:
                result.append(words)
            # 1 大家都在聊
            words = self.get_top_count_words()
            if words is not None:
                result.append(words)

        elif type == 1:
            # 0 表示获取所有的聊天的词汇
            words = self.get_baidu_words()
            if words is not None:
                result.append(words)
        elif type == 2:
            # 0 大家都在聊
            words = self.get_top_count_words()
            if words is not None:
                result.append(words)

        if len(result) > 0:
            self._result = result

    def get_baidu_words(self):
        index = self.get_argument("page_index", default=0)
        words = Words.objects(src_type=1).order_by("+created")[index * 30:(index + 1) * 30]
        if len(words) == 0:
            words = Words.objects(src_type=1).order_by("+created")[0:30]

        if len(words) == 0:
            return None

        result = {"type": 1, "type_name": "热点词汇"}
        word_list = []

        for word in words:
            word_map = {}
            if word.word_type == 1:
                word_map["type"] = "新"

            word_map["word"] = word.word

            word_list.append(word_map)

        result["words"] = word_list

        return result

    def get_top_count_words(self):
        index = self.get_argument("page_index", default=0)
        words = Words.objects().order_by("-user_count")[index * 30:(index + 1) * 30]
        if len(words) == 0:
            words = Words.objects().order_by("-user_count")[0:30]

        if len(words) == 0:
            return None

        result = {"type": 2, "type_name": "大家都在聊"}
        word_list = []

        for word in words:
            word_map = {}
            if word.word_type == 1:
                word_map["type"] = "新"

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
        black_user = BlackUser(user_id=black_user_id)
        User.objects(id=user_id).update_one(pull__black_users=black_user)


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
            self.check_params_exists("text")
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
        report_user.text = self.get_argument("text")

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

# coding=utf-8

__author__ = 'murui'

import tornado.web

from message import MessageUtils
from model import *
import utils
from rong import *


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        connect('project1', host='mongodb://182.92.78.106:27017/test')

    def check_params_exists(self, key):
        """
            判断参数是否存在
        :param key:需要判断的参数
        """
        value = self.get_argument(key, default=None)
        # 判断是否为空
        if value is None:
            raise tornado.web.HTTPError("ERROR_0001", MessageUtils.ERROR_0001, key)


# 用户登录处理
class UserHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
            用户信息的获取
        :return:
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_get_params()
            result = self.get_user_info()

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

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        """
            实际上是做user的login操作
        :return: 处理后的json的数组
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_post_params()
            # 获取登陆用户的信息
            result = self.get_login_user()

        except tornado.web.HTTPError, e:
            code = e.status_code
            message = e.log_message.format(e.args)

        # 将数据整理后
        response = {}

        response["code"] = code
        response["message"] = message
        response["result"] = result

        self.write(json.dumps(response))
        self.finish()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def put(self):
        """
            编辑user的内容，编辑用户的信息
        :return: 返回处理后的json字符串
        """
        code = "200"
        message = ""
        result = ""

        try:
            # 检查参数的传入
            self.check_put_params()
            # 获取登陆用户的信息
            self.edit_user_info()

        except tornado.web.HTTPError, e:
            code = e.status_code
            message = e.log_message.format(e.args)

        # 将数据整理后
        response = {}

        response["code"] = code
        response["message"] = message
        response["result"] = result

        self.write(json.dumps(response))
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

    def check_put_params(self):
        # 判断参数是否存在
        self.check_params_exists("user_id")

    def check_get_params(self):
        # 判断参数是否存在
        self.check_params_exists("user_id")

    def get_user_info(self):
        user_id = self.get_argument("user_id", default=None)
        user = User.objects(id=user_id).only("user_name", "user_photo_url", "user_sex", "user_region", "user_sign",
                                             "user_telephone").first()
        # post = Post.objects.no_dereference().first()
        if user is not None:
            reslut = {}
            reslut["name"] = user.user_name
            reslut["photo"] = user.user_photo_url
            reslut["sex"] = user.user_sex
            reslut["region"] = user.user_region
            reslut["signature"] = user.user_sign
            reslut["phone"] = user.user_telephone

            return reslut

        return ""

    def get_login_user(self):

        # 0,表示微信，1，表示微博，2，表示手机号
        type = int(self.get_argument("type", default=None))
        login_id = self.get_argument("id", default=None)

        user = None
        if type == 2:
            pwd = utils.md5(self.get_argument("pwd", default=None))
            user = User.objects(authen_type=type,
                                login_id=login_id,
                                user_pwd=pwd).first()
        else:
            user = User.objects(authen_type=type,
                                login_id=login_id).first()

        if user is None:
            # 将数据保存到数据库中
            user = User()
            user.authen_type = type
            user.login_id = login_id
            user.user_name = self.get_argument("name", default=None)
            user.user_pwd = utils.md5(self.get_argument("pwd", default=None))
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
            raise tornado.web.HTTPError("ERROR_0003", MessageUtils.ERROR_0003)

        reslut = {}
        reslut["user_id"] = str(user.pk)
        reslut["token"] = token
        return reslut

    def check_post_params(self):

        type = self.get_argument("type", default=None)

        # 判断是否为空
        if type is None:
            raise tornado.web.HTTPError("ERROR_0001", MessageUtils.ERROR_0001, "type")
        # 判断是否在可控的范围内
        if type not in ["0", "1", "2"]:
            raise tornado.web.HTTPError("ERROR_0002", MessageUtils.ERROR_0002, "type")

        id = self.get_argument("id", default=None)
        if id is None:
            raise tornado.web.HTTPError("ERROR_0001", MessageUtils.ERROR_0001, "id")

        pwd = self.get_argument("pwd", default=None)

        if cmp(type, "2") == 0 and pwd is None:
            raise tornado.web.HTTPError("ERROR_0001", MessageUtils.ERROR_0001, "pwd")

        name = self.get_argument("name", default=None)
        if type in ["0", "1"] and name is None:
            raise tornado.web.HTTPError("ERROR_0001", MessageUtils.ERROR_0001, "name")

        photo = self.get_argument("photo", default=None)
        if type in ["0", "1"] and photo is None:
            raise tornado.web.HTTPError("ERROR_0001", MessageUtils.ERROR_0001, "photo")


# 用户登录处理
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
            # result = self.get_user_info()

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

# coding=utf-8

__author__ = 'murui'

from mongoengine import *

# 用户文档
class User(Document):
    # 认证类型，0.表示微信，1.表示微博，2表示手机号单独注册
    authen_type = IntField()
    # type为0,1的场合下，为open_id,2表示的手机号
    login_id = StringField()
    # 用户名称
    user_name = StringField()
    # 用户密码
    user_pwd = StringField()
    # 用户头像地址
    user_photo_url = StringField()
    # 用户性别
    user_sex = StringField()
    # 用户生日
    user_birthday = StringField()
    # 用户身份
    user_region = StringField()
    # 用户签名
    user_sign = StringField()
    # 用户电话
    user_telephone = StringField()
    # 用户状态
    user_status = IntField()


class Paper(Document):
    content = StringField()
    author = ReferenceField(User)

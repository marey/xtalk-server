# coding=utf-8

__author__ = 'murui'

from datetime import datetime

from mongoengine import *


class SysTag(Document):
    # 标签名称
    tag_name = StringField()
    # 排序顺序
    order_by = IntField()
    # 创建时间
    created = DateTimeField(default=datetime.now)


class SysChannel(Document):
    #  频道名称
    channel_name = StringField()
    # 排序顺序
    order_by = IntField()
    # channel_name = ReferenceField(User)
    tags = ListField(ReferenceField(SysTag))
    # 创建时间
    created = DateTimeField(default=datetime.now)


class UserChannel(Document):
    channel_name = StringField()
    # 创建时间
    created = DateTimeField(default=datetime.now)


class BlackUser(EmbeddedDocument):
    # 黑名单的地址
    user_id = StringField()
    # 拖黑时间
    created = DateTimeField(default=datetime.now)


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
    # 用户自定义频道
    channels = ListField(ReferenceField(UserChannel))
    # 用户的黑名单列表
    black_users = ListField(EmbeddedDocumentField(BlackUser))
    # 创建时间
    created = DateTimeField(default=datetime.now)


class State(Document):
    """
        用户状态的内容
    """
    # 图片所在的URL地址
    img_urls = ListField(StringField())
    # 状态的内容
    content = StringField()

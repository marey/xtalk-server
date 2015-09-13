# coding=utf-8

__author__ = 'murui'

from datetime import datetime
from datetime import datetime

from mongoengine import *

class WordGroup(EmbeddedDocument):
    # 群主
    group_user_id = StringField()
    # 创建时间
    created = DateTimeField(default=datetime.now)

class TopWords(Document):
    # 类型
    type = IntField()
    # word_id
    word_id = StringField()
    # 查询的词汇
    word = StringField()
    # 创建时间
    created = DateTimeField(default=datetime.now)
    meta = {
        'indexes': [
            'word_id',
            ('word_id', '-type'),
            {
                'fields': ['created'],
                'expireAfterSeconds': 7200
            }
        ]
    }

class Words(Document):
    # id 是md5加密的
    word_id = StringField()
    # 词条的类型
    # 1.百度热搜
    # 2.个人search
    src_type = IntField()
    # 当前的词汇
    word = StringField()
    # 词汇类型
    # 1:表示新
    word_type = IntField()
    # 该词汇里面的聊天的人数
    user_count = IntField()
    # 用户群组
    user_group = EmbeddedDocumentField(WordGroup)
    # 创建时间
    created = DateTimeField(default=datetime.now)

# 群组的用户列表
class GroupUsers(Document):
    # Word ID
    word_id = StringField()
    # 用户
    users = ListField(EmbeddedDocumentField(WordGroup))

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

class UserWords(EmbeddedDocument):
    # Word的主键
    word_id = ObjectIdField()
    # Word
    word = StringField()
     # 创建Word的时间
    created = DateTimeField(default=datetime.now)

# 用户文档
class User(Document):
    # 认证类型，0.表示微信，1.表示微博，2表示手机号单独注册
    authen_type = IntField()
    # type为0,1的场合下，为open_id,2表示的手机号的MD5加密值
    login_id = StringField()
    # 用户名称
    user_name = StringField()
    # 用户密码
    user_pwd = StringField()
    # 用户头像地址
    user_photo_url = URLField()
    # 用户性别
    user_sex = IntField()
    # 用户生日
    user_birthday = StringField()
    # 用户省份
    user_region = StringField()
    # 用户签名
    user_sign = StringField()
    # 用户电话
    user_telephone = StringField()
    # 用户状态
    user_status = IntField()
    # 融云的token
    rong_token = StringField()
    # 用户的聊天室 tag
    user_words = ListField(EmbeddedDocumentField(UserWords))
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


class OsVersion(Document):
    """
        客户端版本
    """
    # 客户端类型
    os_type = IntField()
    # 版本号
    version = StringField()
    # 创建时间
    created = DateTimeField(default=datetime.now)


# 保存举报用户的记录
class ReportUser(Document):
    report_user_id = StringField()
    # 黑名单的地址
    user_id = StringField()
    # 被举报的类型
    type = IntField()
    # 所在的群组
    group_id = StringField()
    # 举报时间
    created = DateTimeField(default=datetime.now)

# 保存系统的一个设定信息
class SysSetting(Document):
    # 背景图片的地址
    main_back_img = StringField()
    # 七牛的token
    qiniu_token = StringField()
    # 七牛的的token有效时间
    qiniu_token_expires_time = DateTimeField()
    # 创建时间
    created = DateTimeField(default=datetime.now)
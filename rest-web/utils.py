# coding=utf-8
__author__ = 'murui'


# md5 加密
def md5(key):
    import hashlib
    m = hashlib.md5()
    m.update(key)
    return m.hexdigest()

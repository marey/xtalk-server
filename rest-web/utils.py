# coding=utf-8
__author__ = 'murui'
import re

# md5 加密
def md5(key):
    import hashlib
    m = hashlib.md5()
    m.update(key)
    return m.hexdigest()

def check_mobile_phone(phone_number):
    regex = re.compile(r'1\d{10}', re.IGNORECASE)
    phonenums = re.findall(regex, phone_number)
    if len(phonenums) == 0:
        return None
    else:
        return phonenums[0]

# print(check_mobile_phone("1380018000"))
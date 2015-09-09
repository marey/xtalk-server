# coding=utf-8

__author__ = 'murui'
import hashlib

if __name__ == '__main__':
    # unittest.main()

    value = "郑州大妈街头打人"
    login_id = "15652376134"
    md5obj = hashlib.md5()
    md5obj.update(login_id)
    print md5obj.digest()
    hash = md5obj.hexdigest()
    print hash

    test = {value: "1"}
    print test

# coding=utf-8

__author__ = 'murui'
import hashlib

if __name__ == '__main__':
    # unittest.main()

    value = "郑州大妈街头打人"
    md5obj = hashlib.md5()
    md5obj.update(value)
    print md5obj.digest()
    hash = md5obj.hexdigest()
    print hash

    test = {value: "1"}
    print test

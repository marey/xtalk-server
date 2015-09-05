# coding=utf-8

__author__ = 'murui'

from model import *

from handler import BaseHandler
import datetime
import utils


class MainHandler(BaseHandler):
    def get(self):
        self.render("login.html")


class WebMainLeftHandler(BaseHandler):
    def get(self):
        self.render("left.html")


class WebMainTopHandler(BaseHandler):
    def get(self):
        self.render("top.html")


class WebMainIndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class WebLoginHandler(BaseHandler):
    def post(self):
        user_name = self.get_argument("user_name")
        user_pwd = self.get_argument("user_pwd")
        self.render("main.html")


class WebWordsGetHandler(BaseHandler):
    def get(self):
        self.render("right.html")


class WebWordsAddHandler(BaseHandler):
    def get(self):
        word = self.get_argument("word")

        word_id = utils.md5(word)
        record_word = Words.objects(word_id=word_id).first()
        if record_word is not None:
            self.write("该词条已经存在！")
        else:
            word_type = int(self.get_argument("word_type",default=1))
            record_word = Words()

            record_word.word_id = word_id
            record_word.word = word
            record_word.src_type = word_type
            record_word.word_type = 1
            record_word.save()

            top_flg = int(self.get_argument("word_type",default=1))
            if top_flg == 1:
                top_word = TopWords()
                top_word.type = record_word.src_type
                top_word.word_id = record_word.word_id
                top_word.word = record_word.word
                top_word.save()

            self.write("词条添加成功！")
            self.finish()


class WebWordIndexHandler(BaseHandler):
    def get(self):
        result = []
        words = Words.objects(src_type=1).order_by('-created')[:100]
        for word in words:
            result.append(
                {"id": str(word.id), "word_id": word.word_id, "word": word.word,
                 "created": word.created.strftime('%Y-%m-%d %H:%M:%S')})

        self.render("words/baidu_search_index.html", items=result, key_word="",
                    top_key_word="")


class WebWordAddTopHandler(BaseHandler):
    def get(self):
        param_id = self.get_argument("id")

        result = []
        word = Words.objects(id=param_id).first()

        if word is not None:
            top_word = TopWords.objects(word_id=word.word_id).first()
            if top_word is None:
                top_word = TopWords()
                top_word.type = word.src_type
                top_word.word_id = word.word_id
                top_word.word = word.word
                top_word.save()
            else:
                top_word.created = datetime.datetime.now()
                top_word.save()

            self.write("置顶成功！")
            self.finish()

class WebWordTopDelHandler(BaseHandler):
    def get(self):
        param_id = self.get_argument("id")
        TopWords.objects(id=param_id).delete()
        self.write("删除成功！")
        self.finish()


class WebWordSearchHandler(BaseHandler):
    def get(self):
        key_word = self.get_argument("key_word", default="")
        type = int(self.get_argument("word_type", default=1))
        result = []
        words = None
        if len(key_word) == 0:
            words = Words.objects(src_type=type).order_by('-created')[:100]
        else:
            words = Words.objects(src_type=type, word__icontains=key_word).order_by('-created')

        data_list = []

        if words is not None and len(words) > 0:
            for word in words:
                data_list.append([word.word_id, word.word.encode("utf8"),
                                  word.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  str(word.id)])

        self.write({"data": data_list, "draw": 0, "recordsTotal": len(data_list), "recordsFiltered": len(data_list)})

        self.finish()


class WebWordTopSearchHandler(BaseHandler):
    def get(self):

        key_word = self.get_argument("top_key_word", default="")
        type = int(self.get_argument("top_word_type", default=1))
        result = []
        words = None
        if len(key_word) == 0:
            words = TopWords.objects(type=type).order_by('-created')[:100]
        else:
            words = TopWords.objects(type=type, word__icontains=key_word).order_by('-created')

        data_list = []

        if words is not None and len(words) > 0:
            for word in words:
                down_time = word.created + datetime.timedelta(hours=2)
                data_list.append([word.word_id, word.word.encode("utf8"),
                                  word.created.strftime('%Y-%m-%d %H:%M:%S'),
                                  down_time.strftime('%Y-%m-%d %H:%M:%S'),
                                  str(word.id)])

        self.write({"data": data_list, "draw": 0, "recordsTotal": len(data_list), "recordsFiltered": len(data_list)})

        self.finish()

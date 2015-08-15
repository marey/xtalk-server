# coding=utf-8
__author__ = 'murui'
import scrapy
from bs4 import BeautifulSoup
from model import *
import hashlib
from bson.objectid import ObjectId
from datetime import datetime


class BaiDuSpider(scrapy.Spider):
    name = "x_talk"
    start_urls = ['http://top.baidu.com/buzz?b=1']
    # 连接mongo
    connect('project1', host='mongodb://127.0.0.1:27017/test')

    def parse(self, response):
        # soup = BeautifulSoup(response.body, 'html.parser')
        soup = BeautifulSoup(response.body)
        news_list = soup.find_all("td", class_="keyword")
        for news in news_list:
            news_title = news.a.string.encode("utf8")
            md5obj = hashlib.md5()
            md5obj.update(news_title)
            word_id = md5obj.hexdigest()
            word = Words.objects(word_id=word_id).first()
            if word is None:
                word = Words()

            word.word_id = word_id
            word.word = news_title
            word.src_type = 1
            if news.span is not None:
                word.word_type = 1
            else:
                word.word_type = None

            word.created = datetime.now

            word.save()

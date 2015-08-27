# coding=utf-8

__author__ = 'murui'

import tornado.web
from bson.objectid import ObjectId

from message import MessageUtils
from model import *
import utils
from rong import *

from handler import BaseHandler

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
        print user_name,user_pwd
        self.render("main.html")
#-*-coding:utf-8 -*-

import urllib, hashlib
import tornado.web
from models.user import User
from models.user_feed import UserFeed
from BaseHandler import BaseHandler
from .util import DataTimeEncoder
import json
import logging


class FeedHandler(BaseHandler):
    def post(self):

        self.user = self.get_current_user()
        if self.user == None:
            self.redirect("/login")

        self.site_url = self.get_argument("site_url", default=None)

        page = self.get_argument("page", default=1)
        self.offset = (int(page) - 1) * 20
        entries = []

        if self.site_url == "love":
            entries = self.get_love_entries()
        else:
            entries = self.get_feed_entries()
        self.set_json_type()
        self.write(json.dumps(entries, cls=DataTimeEncoder))

    def get_love_entries(self):

        return self.user.get_love_entries(self.offset)


    def get_feed_entries(self):
        return self.user.get_page_entries(self.site_url, self.offset)
        
            
            
            
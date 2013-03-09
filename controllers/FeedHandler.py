#-*-coding:utf-8 -*-

import urllib, hashlib
import tornado.web
from models.user import User
from models.user_feed import UserFeed
from BaseHandler import BaseHandler

from tornado.escape import json_encode

    
class FeedHandler(BaseHandler):
    
    def get(self, site_url):
        
        user = self.get_current_user()
        if user == None:
            self.redirect("/login")
        
        
        
        
        

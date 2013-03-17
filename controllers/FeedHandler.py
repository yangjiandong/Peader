#-*-coding:utf-8 -*-

import urllib, hashlib
import tornado.web
from models.user import User
from models.user_feed import UserFeed
from BaseHandler import BaseHandler

import datetime
import json

class DataTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return json.JSONEncoder.default(self, obj)

 
    

    
    

    
class FeedHandler(BaseHandler):
    
   
    def post(self):
        
        user = self.get_current_user()
        if user == None:
            self.redirect("/login")
        
        site_url = self.get_argument("site_url", default = None)
        
        page = self.get_argument("page", default = 1)
        offset = (int(page)-1) * 20
        entries  =user.get_page_entries(site_url, offset)
        self.set_json_type()
        self.write(json.dumps(entries, cls = DataTimeEncoder))
              
        
  
            
            
            
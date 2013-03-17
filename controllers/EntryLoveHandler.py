#-*-coding:utf-8 -*-

import urllib, hashlib
import tornado.web
from models.user import User
from models.entry import Entry
from models.user_feed import UserFeed
from models.user_entry import UserEntry
from models.model import Model
from BaseHandler import BaseHandler
from tornado.escape import json_encode
    
class EntryLoveHandler(BaseHandler):
    
   
    def get(self):
        user = self.get_current_user()
        if user == None:
            self.redirect("/login")
        entry_id = int(self.get_argument("entry_id"))
        love = int(self.get_argument("love"))
        user.label_love(entry_id, love)
        self.write("ok")
       
    
   
  
        
        
        
        
        
        
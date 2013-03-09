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
import tornado.web
import tornado.gen
    
class GroupHandler(BaseHandler):
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        
        user = self.get_current_user()
        if user == None:
            self.redirect("/login")
            
        groups  = yield tornado.gen.Task(self.update_user_entry, user)
        self.set_json_type()
        self.write(json_encode(groups))
        self.finish()
       
    
    def update_user_entry(self, user, callback=None):
        
        user_feed = UserFeed()
        feeds =  user_feed.get_all_by_user(user['id'])
        
        for feed in feeds:
           entries = Entry.get_new_entries(feed['site_url'], feed['updated_at'])
           user_entries = []
           for entry in entries:
               user_entries.append((entry['id'], user['id'],entry['site_url'] ))
           if len(user_entries) > 0:
               UserEntry.insert_entries(user_entries)
           user.update_feed_update_at(feed['site_url'])
           
        
        groups = user.get_groups()
        callback(groups )
        
  
        
        
        
        
        
        
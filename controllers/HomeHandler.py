#-*-coding:utf-8 -*-

import urllib, hashlib
import tornado.web
from models.user import User
from models.user_feed import UserFeed
from BaseHandler import BaseHandler

from .util import make_gravatar_url
    
class HomeHandler(BaseHandler):
    
    def get(self):
        
        user = self.get_current_user()
        if user == None:
            self.redirect("/login")
        else:
            self.render("index.html", user = user, gravatar_for = make_gravatar_url)
    
    def update_user_entry(self, user_id):
        user_feed = UserFeed()
        feeds =  user_feed.get_all_by_user(user_id)
        
        for feed in feeds:
           entries = Entry.get_new_entries(feed['site_url'], feed['updated_at'])
           user_entries = []
           for entry in entries:
               user_entries.append((entry['id'], user_id))
               UserEntry.insert_entries(user_entries)
               
        
        
        
        
        
        
        
        
        
        
        
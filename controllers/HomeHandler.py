#-*-coding:utf-8 -*-

import urllib, hashlib
import tornado.web
from models.user import User
from models.user_feed import UserFeed
from BaseHandler import BaseHandler

def make_gravatar_url(email):
    #这里需要配置成在主机的默认头像
    default = "http://farm9.staticflickr.com/8096/8519545439_459f63bf5b_t_d.jpg"
    size = 60
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url
    
class HomeHandler(BaseHandler):
    
    def get(self):
        
        user = self.get_current_user()
        if user == None:
            self.redirect("/login")
        
       
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
               pprint.pprint(entry)
        
        
        
        
        
        
        
        
        
        
        
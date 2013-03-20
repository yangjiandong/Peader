#-*-coding:utf-8 -*-

import tornado.web
from models.user import User

from BaseHandler import BaseHandler

class LogoutHandler(BaseHandler):
    
    def get(self):
        
        user = self.get_current_user()
        if user:
            self.clear_cookie("member_auth")
        
        self.redirect('/login')
      
        
    
    
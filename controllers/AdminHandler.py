#-*-coding:utf-8 -*-

import tornado.web
from models.user import User

from BaseHandler import BaseHandler
from .util import make_gravatar_url


class AdminHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if user:
            self.render("admin.html", user=user, gravatar_for=make_gravatar_url)

        self.redirect('/login')
      
        
    
    
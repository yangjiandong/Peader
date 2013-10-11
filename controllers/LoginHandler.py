#-*-coding:utf-8 -*-

import tornado.web
from models.user import User

from BaseHandler import BaseHandler

class LoginHandler(BaseHandler):
    
    def get(self):
        
        user = self.get_current_user()
        if user == None:
            self.render("login.html")
        else:
            self.redirect('/')
       # self.set_secure_cookie("member_auth", user['email'])
        
    
    def post(self):
        
        email = self.get_argument("Email", default = None)
        password = self.get_argument("Password", default = None)
        
        user = User.find_by_email_and_password(email, password)
        #self.write(user['email'])
        self.set_secure_cookie("member_auth", user['email'])
        self.redirect('/')
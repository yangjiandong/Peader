#-*-coding:utf-8 -*-

import tornado.web
from controllers import BaseHandler
from models.user import User



class RegisterHandler(BaseHandler.WebBaseHandler):
    
    def get(self):
        
        self.render("register.html")
    
    def post(self):
        
        email = self.get_argument("Email", default = None)
        password = self.get_argument("Password", default = None)
        User.create(email, password)
        self.write("Email: " + email +" Password: "  + password)
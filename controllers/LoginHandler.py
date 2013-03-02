#-*-coding:utf-8 -*-

import tornado.web
from models.user import User



class LoginHandler(tornado.web.RequestHandler):
    
    def get(self):
        
        self.render("login.html")
    
    def post(self):
        
        email = self.get_argument("Email", default = None)
        password = self.get_argument("Password", default = None)
        user = User()
        user.find_by_email_and_password(email, password)
        
        self.write("Email: " + user["email"])
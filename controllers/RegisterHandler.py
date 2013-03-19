#-*-coding:utf-8 -*-

import tornado.web
from controllers import BaseHandler
from models.user import User
import logging
from .util import EmailIsValid, PasswdIsValid
import tornado.web
import tornado.gen

class RegisterHandler(BaseHandler.BaseHandler):
    
    def get(self):
        user = self.get_current_user()
        if user == None:
            self.render("register.html")
        self.redirect('/')
        
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        
        successed  = yield tornado.gen.Task(self.create_user)    
        self.set_secure_cookie("member_auth", self.email)
        self.redirect('/')
        self.finish()
        
    def create_user(self,  callback=None):
        self.email = self.get_argument("Email", default = None)
        password = self.get_argument("Password", default = None)
        verify_password = self.get_argument("VerifyPassword", default = None)
        successed = False
        if EmailIsValid(self.email) and  password == verify_password and PasswdIsValid(password):
            successed  = User.create(self.email, password)
        callback(successed)
            
        
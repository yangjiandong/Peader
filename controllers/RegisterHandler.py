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
        else:
            self.redirect('/')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        logging.info('register post...')

        successed = yield tornado.gen.Task(self.create_user)
        self.set_secure_cookie("member_auth", self.email)
        self.redirect('/')

    #        self.finish()

    def create_user(self, callback=None):
        logging.info('register ,create_user ...')
        import os
        #logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG,
        #                    filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')

        self.email = self.get_argument("Email", default=None)
        password = self.get_argument("Password", default=None)
        verify_password = self.get_argument("VerifyPassword", default=None)
        logging.info(self.email)

        successed = False

        if EmailIsValid(self.email) and password == verify_password and PasswdIsValid(password):
            logging.info('EmailIsValid...')
            user = User.find_by_email_and_password(self.email, password)
            if user.empty:
                logging.info('User create...')
                logging.info(self.email)
                successed = User.create(self.email, password)
        else:
            logging.info('no create user...')

        logging.info('register ,create_user, successed ...')
        logging.info(successed)

        callback(successed)



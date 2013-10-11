#-*-coding:utf-8 -*-

import tornado.web
from models.user import User


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(404)
        self.write('{"status":"error","msg":"Page not found"}')


    def get_error_html(self, status_code, **kwargs):
        self.write(self.render_string("404.html"))

    #        if status_code == 404:
    #            self.write(self.render_string("404.html"))
    #        else:
    #            return tornado.web.RequestHandler.get_error_html(self, status_code,
    #                                                             **kwargs)
    #


    def get_current_user(self):
        email = self.get_secure_cookie("member_auth")
        if not email: return None

        user = User.find_by_email(email)
        return user


    def _on_auth(self):
        pass

    def set_json_type(self):
        self.set_header("Content-Type", "application/json")
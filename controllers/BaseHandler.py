#-*-coding:utf-8 -*-

import tornado.web
from models.user import User


    
class WebBaseHandler(tornado.web.RequestHandler):
    
    def get(self):
        
        self.set_status(404)
        self.write('{"status":"error","msg":"Page not found"}')
        
    @property
    def db_settings(self):
        
             return self.application.db_settings
         
             
    
    
    
    def get_current_user(self):
        #self.setJsonType()
        email = self.get_secure_cookie("member_auth")
        if not email: return None
        current_user = User(db_settings)
    
    
    def _on_auth(self):
        pass
    
    def setJsonType(self):
        self.set_header("Content-Type", "application/json")
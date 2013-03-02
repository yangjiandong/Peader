#-*-codeing:utf-8 -*-

import urllib, hashlib

import tornado.web

class AvatarHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("avatar.html", gravatar_url = None)
        
    
    def post(self):
        
        email = self.get_argument("Avatar", None)
        
        self.render("avatar.html", gravatar_url = self._make_gravatar_url(email))
        
    
    def _make_gravatar_url(self, email):
        
        #这里需要配置成在主机的默认头像
        default = "http://farm9.staticflickr.com/8096/8519545439_459f63bf5b_t_d.jpg"
        size = 60
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url

        
        


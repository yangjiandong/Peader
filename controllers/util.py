#-*-coding:utf-8 -*-

import datetime
import json
import tornado.web
import re
import hashlib
import urllib
import feedparser

class DataTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return json.JSONEncoder.default(self, obj)

def make_gravatar_url(email ,size = 60):
    #这里需要配置成在主机的默认头像
    default = "http://farm9.staticflickr.com/8096/8519545439_459f63bf5b_t_d.jpg"
    
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url


    
def EmailIsValid(email):
    if len(email) > 5:
        return True
    
    return False

def PasswdIsValid(passwd):
    if  5 < len(passwd) < 17:
        return True
    
    return False

def URLValidator(url):
    
    url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
      #  r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if url_regex.match(url):
        return True
    
    return False


def SubscribeValidator(subscribe):
    
    feed = feedparser.feedparser(subcribe)
    
    if 'version' in feed and feed['version'] != '':
        return True
    
    return False
   
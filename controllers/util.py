#-*-coding:utf-8 -*-

import datetime
import json
import tornado.web
import re
import feedparser

class DataTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return json.JSONEncoder.default(self, obj)




    
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
   
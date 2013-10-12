#-*-coding:utf-8 -*-

import datetime
import json
import tornado.web
import re
import hashlib
import urllib
import feedparser
import sys
import time

#把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d-%H")

#把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d-%H")

#把字符串转成时间戳形式
def string_toTimestamp(strTime):
    return time.mktime(string_toDatetime(strTime).timetuple())

#把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))

#把datetime类型转外时间戳形式
def datetime_toTimestamp(dateTim):
    return time.mktime(dateTim.timetuple())

def func_name_and_line():
    """异常得到代码片段的信息."""
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return f.f_code.co_name, f.f_lineno

def test():
    print func_name_and_line()

class DataTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return json.JSONEncoder.default(self, obj)


def make_gravatar_url(email, size=60):
    #这里需要配置成在主机的默认头像
    default = "http://farm9.staticflickr.com/8096/8519545439_459f63bf5b_t_d.jpg"

    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
    return gravatar_url


def EmailIsValid(email):
    if len(email) > 5:
        return True

    return False


def PasswdIsValid(passwd):
    if 5 < len(passwd) < 17:
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
   
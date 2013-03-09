#-*-coding:utf-8 -*-

import urllib, hashlib
import tornado.web
from models.user import User
from models.entry import Entry
from models.user_feed import UserFeed
from models.user_entry import UserEntry
from models.model import Model

import pprint

class UserFeedUpdate:
    def __init__(self ,user_id):
        user_feed = UserFeed()
        feeds =  user_feed.get_all_by_user(user_id)
        
        for feed in feeds:
           entries = Entry.get_new_entries(feed['site_url'], feed['updated_at'])
           user_entries = []
           for entry in entries:
               user_entries.append((entry['id'], user_id))
               UserEntry.insert_entries(user_entries)
               pprint.pprint(entry)
           

from config.settings import *



db_settings = dict(
                               use_unicode = True, 
                                   charset = "utf8",
                                      host = options.mysql_host, 
                                        db = options.mysql_database,
                                     user  = options.mysql_user, 
                                    passwd = options.mysql_password,
                               )
Model.initailize(db_settings)

UserFeedUpdate(1)
    
    
    
    
#-*-coding:utf-8 -*-
#!/usr/bin/python

from .model import Model
from .user import User
import MySQLdb
import logging

from tornado.escape import json_encode

class UserFeed(Model):
    """用户类，用于登录，注册，认证等
               密码加密使用sha224和加盐保护"""   
                
    def __init__(self):
        
        Model.__init__(self)
        
    @staticmethod
    def find_all_by_user(user_id):
        user_feed = UserFeed()
        feeds = user_feed._get_all_by_user(user_id)
        
        return feeds
        
 
    def _get_all_by_user(self, user_id): 
        
        feeds = None
        cursor = self.cursor()
        try:
            command = cursor.execute("""SELECT `site_url`, `name`, `site_group` \
                            FROM `rss_user_feeds` WHERE `user_id` = %s \
                            ORDER BY site_group""" ,(user_id))
            
            feeds = cursor.fetchone()
        except MySQLdb.Error, e:
         
            logging.error("Query user feeds Failed error : %s", e.args[1])
        
        finally:
            cursor.close()
            
        return feeds
        
    def _create(self, email, password):
        
        
        return True
        
  
        
        
        
        

        



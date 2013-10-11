#-*-coding:utf-8 -*-
#!/usr/bin/python

from .model import Model
from .user import User
import MySQLdb
import logging

from tornado.escape import json_encode


class UserFeed(Model):
    def __init__(self):

        Model.__init__(self)

    @staticmethod
    def find_all_by_user(user_id):
        user_feed = UserFeed()
        feeds = user_feed._get_all_by_user(user_id)

        return feeds


    @staticmethod
    def find_by_site_url_and_user(site_url, user_id):
        user_feed = UserFeed()
        user_feed._find_by_site_url_and_user(site_url, user_id)
        return user_feed


    def _find_by_site_url_and_user(self, site_url, user_id):


        cursor = self.cursor()
        try:
            command = cursor.execute("""SELECT `site_url`, `name`, `site_group` \
                            FROM `rss_user_feeds` WHERE `site_url` = %s and `user_id` = %s""",
                                     (site_url, user_id))

            self._data = cursor.fetchone()
        except MySQLdb.Error, e:

            logging.error("Query user feeds Failed error : %s", e.args[1])

        finally:
            cursor.close()


    def get_all_by_user(self, user_id):

        feeds = None
        cursor = self.cursor()
        try:
            command = cursor.execute("""SELECT `site_url`, `name`, `updated_at` \
                            FROM `rss_user_feeds` WHERE `user_id` = %s \
                            """, (user_id))

            feeds = cursor.fetchall()
        except MySQLdb.Error, e:

            logging.error("Query user feeds Failed error : %s", e.args[1])

        finally:
            cursor.close()

        return feeds

    def _create(self, email, password):


        return True
        
  
        
        
        
        

        



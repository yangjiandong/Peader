#-*-coding:utf-8 -*-
#!/usr/bin/python

from model import Model
import hashlib
import MySQLdb
import logging

from time import  strftime, gmtime

class User(Model):
    """用户类，用于登录，注册，认证等
               密码加密使用sha224和加盐保护"""   
                
    def __init__(self):
        
        Model.__init__(self)
        
    @staticmethod
    def find_by_email(email):
        
        user = User()
        user._find_by_email(email)
        return user
 
    @staticmethod  
    def find_by_email_and_password(email, password ):
        
        user = User()
        user._on_auth(email)
        if user._data and user._check_password(password):
            return user
        #not aut
        user._data = None
        return user
    
    def update_feed_update_at(self, site_url):
        cursor =  self.cursor()
        try:
            cursor.execute("UPDATE `rss_user_feeds`\
                        SET `updated_at`=NOW()\
                        WHERE `user_id`=%s AND `site_url`=%s", 
                                (self['id'], site_url))
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("update user feed   Failed error : %s", e.args[1])
        finally:
            cursor.close()
    
    def label_read(self, entry_id, read = 1): 
        
        cursor =  self.cursor()
        try:
            cursor.execute("UPDATE `rss_user_entries` \
                        SET `read`=%s \
                        WHERE `user_id`=%s AND `entry_id`=%s", 
                                (read, self['id'], entry_id))
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("update rss_user_entries  Failed error : %s", e.args[1])
        finally:
            cursor.close()
    def label_love(self, entry_id, love): 
        
        cursor =  self.cursor()
        try:
            cursor.execute("UPDATE `rss_user_entries` \
                        SET `love`=%s \
                        WHERE `user_id`=%s AND `entry_id`=%s", 
                                (love, self['id'], entry_id))
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("update rss_user_entries love  Failed error : %s", e.args[1])
        finally:
            cursor.close()
    
    def get_love_entries(self, offset): 
         logging.error("what worng?")
         return self.query("SELECT  `rss_user_entries`.`entry_id`, `title`, `link`, `description`, `created_at` , `read`, `love` \
                    FROM `rss_user_entries` INNER JOIN `rss_site_entries` \
                    ON `rss_user_entries`.`entry_id` = `rss_site_entries`.`id` \
                    WHERE user_id = 1 AND `rss_user_entries`.`love` = 1 \
                    ORDER BY `rss_site_entries`.`created_at` DESC \
                    LIMIT 0, 20")
         
    def get_page_entries(self, site_url, offset):
        
        return self.query("SELECT  `rss_user_entries`.`entry_id`, `title`, `link`, `description`, `created_at` , `read`, `love` \
                    FROM `rss_user_entries` INNER JOIN `rss_site_entries` \
                    ON `rss_user_entries`.`entry_id` = `rss_site_entries`.`id` \
                    WHERE user_id = %s AND `rss_user_entries`.`site_url` = %s \
                    ORDER BY `rss_site_entries`.`created_at` DESC \
                    LIMIT %s, 20", self['id'],  site_url, offset)
    
        
    def get_group_feeds(self, site_group):
        cursor =  self.cursor()
        
        try:
            if site_group :
                cursor.execute("SELECT `site_url`, `name`\
                                FROM `rss_user_feeds` \
                                WHERE `user_id` = %s AND `site_group` = %s\
                                GROUP BY `site_url`", 
                                (self['id'], site_group))
            else:
                cursor.execute("SELECT `site_url`, `name`\
                                FROM `rss_user_feeds`\
                                WHERE `user_id` = %s  AND `site_group` IS NULL", 
                                (self['id']))
                
            
            site_feeds = cursor.fetchall()
            
        except MySQLdb.Error, e:
            logging.error(" query  group feeds Failed error : %s", e.args[1])
        finally:
            cursor.close()
            
        group = { "site_group" : site_group, "feeds" : site_feeds}
        return group
    
    def get_groups(self):
        
        cursor =  self.cursor()
        
        try:
            command = cursor.execute("SELECT `rss_user_feeds`.`site_group`,`rss_user_feeds`.`site_url`, \
                        `rss_user_feeds`.`name` , COUNT(`rss_user_feeds`.`site_url`) AS `entry_count` \
                        FROM `rss_user_feeds` INNER JOIN `rss_user_entries` \
                        ON `rss_user_feeds`.`user_id` = `rss_user_entries`.`user_id` AND `rss_user_feeds`.`site_url` = `rss_user_entries`.`site_url` \
                        WHERE `rss_user_feeds`.`user_id` = %s  AND `rss_user_entries`.`read` = 0 \
                        GROUP BY `rss_user_feeds`.`site_url` \
                        ORDER BY `rss_user_feeds`.`site_group` DESC;", (self['id']))
            
            groups = cursor.fetchall()
        except MySQLdb.Error, e:
         
            logging.error("query entry Failed error : %s", e.args[1])
        
        finally:
            cursor.close()
        
        return groups
        
       
    def _on_auth(self, email):
        cursor = self.cursor()
        try:
            command = cursor.execute("""SELECT `id`, `email`, `encrypted_password`, `password_salt` FROM `rss_users` WHERE `email` = %s""" ,(email))
            if command == 1:
                self._data = cursor.fetchone()
        except MySQLdb.Error, e:
         
            logging.error("Insert entry Failed error : %s", e.args[1])
        
        finally:
            cursor.close()
            
    def _find_by_email(self, email): 
        cursor = self.cursor()
        try:
            command = cursor.execute("""SELECT `id`, `email` FROM `rss_users` WHERE `email` = %s""" ,(email))
            if command == 1:
                self._data = cursor.fetchone()
        except MySQLdb.Error, e:
         
            logging.error("Insert entry Failed error : %s", e.args[1])
        
        finally:
            cursor.close()
        
        
                
       
    def _check_password(self, submitted_password):
        return self._data["encrypted_password"] == self._secure_hash("%s--%s" %(self._data["password_salt"], submitted_password ))
    
    
    def _encrypt_password(self, submmited_password):
        
        if not hasattr(self, "_salt"):
            self._salt = self._make_salt(submmited_password)
        
        return self._encrypt(submmited_password)
    
    def _encrypt(self, text):
        return self._secure_hash("%s--%s" %(self._salt, text))
    
    def _secure_hash(self, text):
        
        return hashlib.sha224(text).hexdigest()
    
    def _make_salt(self, text):
        
        return self._secure_hash(strftime('%Y-%m-%d %H:%M:%S UTC', gmtime()) + "--" + text)
    
    
    
    def _create(self, email, password):
        
        encrypted_password = self._encrypt_password(password)
        
        cursor = self.cursor()
        try:
            cursor.execute("""INSERT INTO `rss_users` VALUE(NULL, %s, %s, %s, NULL, NULL, 0) """, (email, encrypted_password , self._salt))
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("create user failed error : %s", e.args[1])
            return False
        
        return True
        
       
    @staticmethod
    def create(email, password):
        
        user = User()
        user._create(email, password)
        
        
        
        

        



#-*-coding:utf-8 -*-
#!/usr/bin/python

from model import Model
import hashlib
import MySQLdb
import logging

from time import  strftime, gmtime

class UserSite(Model):
    """用户类，用于登录，注册，认证等
               密码加密使用sha224和加盐保护"""   
                
    def __init__(self):
        
        Model.__init__(self)
    
        
    @staticmethod
    def find_all_by_user_id(user_id):
        
         = User()
        user._find_by_email(email)
        return user
 
    
    
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
        
        
                
    
       
    
    
    
    
    def _create(self, email, password):
        
        encrypted_password = self._encrypt_password(password)
        
        cursor = self.cursor()
        try:
            cursor.execute("""INSERT INTO `rss_users` VALUE(NULL, '%s', '%s', '%s', NULL, NULL, 0) """ %(email, encrypted_password , self._salt))
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("Fetch Failed error : %s", e.args[1])
            return False
        
        return True
        
       
    @staticmethod
    def create(email, password):
        
        user = User()
        user._create(email, password)
        
        
        
        

        



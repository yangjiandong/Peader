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
        
        
        
        

        



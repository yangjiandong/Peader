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
        self.user = None
        
        
    def find_by_email_and_password(self, email, password ):
        
        cursor = self.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("""SELECT * FROM rss_users WHERE `email` = '%s'""" %(email))
        
        except MySQLdb.Error, e:
            logging.error("Fetch Failed error : %s", e.args[1])
            
        self.user = cursor.fetchone()
        if self.user and self._check_password(password):
            return self.user
        
        #not aut
        return None
    
    def find_by_email(self, email):
        cur = self.cursor()
        query_statement = """SELECT * FROM `rss_users` WHERE `email` = '%s'"""
        command = cur.execute(query_statement %(email))
        return cur.fetchone()
       
    def _check_password(self, submitted_password):
        return self.user["encrypted_password"] == self._secure_hash("%s--%s" %(self.user["password_salt"], submitted_password ))
    
    
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
        
        
        
        

        



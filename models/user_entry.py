#-*-coding:utf-8 -*-
#!/usr/bin/python

from model import Model
import hashlib
import MySQLdb
import logging

from time import  strftime, gmtime

class UserEntry(Model):
    
                
    def __init__(self):
        
        Model.__init__(self)
    
    
    def save(self):
       
        return True
    
    def _insert_entries(self, entries):
        
        cursor = self.cursor()
        try:
            cursor.executemany("""INSERT INTO `rss_user_entries` VALUES(%s, %s, %s, 0, 0, NULL) """, entries)
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("insert new user entries error : %s", e.args[1])
            return False
        
        return True
        
       
    @staticmethod
    def insert_entries(entries):
        
        user_entry = UserEntry()
        return user_entry._insert_entries(entries)
        
        
        

        



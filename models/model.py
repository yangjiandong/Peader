#!/usr/bin/python

import copy
import MySQLdb.constants
import MySQLdb.converters
import MySQLdb.cursors

import logging
import time
 

class Model:
    
    @staticmethod
    def initailize(database_setting):
        if not hasattr(Model, "_db_settings"):
            Model._db_settings = database_setting

    
    @staticmethod
    def initailized():
        """Returns true if the class variable _db_settings has been created."""
        print Model._db_settings
        return hasattr(Model, "_db_settings")
            
        
    def __init__(self):
        
        self.host = Model._db_settings["host"]
        self._db = None
        self._data = None
        self.max_idle_sec = 25200
        self._last_use_sec = time.time()
        
        try:
            self.reconnect()
        
        except Exception:
            logging.error("Cannot connect MySQL on %s", self.host, exc_info = True)
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __del__(self):
        self.close()
    
    def close(self):
        
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None
    
    def reconnect(self):
        
        self.close()
        self._db = MySQLdb.connect(**Model._db_settings)
        print self._db
    
    def commit(self):
        self._db.commit()
    
    def rollback(self):
        self._db.rollback()
        
    def cursor(self, cursorType = MySQLdb.cursors.DictCursor):
        self._ensure_connected()
        if cursorType == None:
            return self._db.cursor()
        
        return self._db.cursor(cursorType)
        
    
    def _ensure_connected(self):
        
        if self._db is None and (time.time() - self._last_use_sec > self.max_idle_sec):
            self.reconnect()
        
        self._last_use_sec = time.time()  
        
    @property  
    def empty(self):  
        is_empty = False
        if self._data == None:
            is_empty = True 
        return is_empty
        
    @staticmethod
    def create():
        raise NotImplementedError("create")
    
    def destory():
        
        raise NotImplementedError("destory")
    
    

        
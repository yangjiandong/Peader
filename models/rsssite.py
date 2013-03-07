#-*-coding:utf-8 -*-
#!/usr/bin/python


from model import Model
from binascii import crc32
import MySQLdb
import logging

from time import  strftime, gmtime

class RssSite(Model):
    
    def __init__(self):
        
        Model.__init__(self)
    
    
    @staticmethod
    def get_site_count():
        rss_site = RssSite()
        cursor = rss_site.cursor(MySQLdb.cursors.Cursor)
        try:
            cursor.execute("SELECT COUNT(*) AS `site_count`  FROM `rss_sites`",)
            site_count = cursor.fetchone()

            
        except MySQLdb.Error, e:
            logging.error("query falied Failed error : %s", e.args[1])
        
        finally:
            cursor.close()
        return site_count[0]
    
    @staticmethod
    def new(data):
        rss_site = RssSite()
        rss_site ._data =data
        
        return rss_site
    
    @staticmethod
    def find_by_url( url):
        
        rss_site = RssSite()
        cursor = rss_site.cursor(MySQLdb.cursors.DictCursor)
        try:
            
            cursor.execute("SELECT `url`, `name`, `content_md5` FROM `rss_sites` force index(`url_crc32`) \
                           WHERE `url_crc32` = CRC32(%s) AND `url` = %s",
                           (url, url))
            rss_site ._data = cursor.fetchone()
            logging.debug("DD %s", rss_site ._data['url'] )
            
        except MySQLdb.Error, e:
            logging.error("Insert entry Failed error : %s", e.args[1])
        
        finally:
            cursor.close()
        
        return rss_site
        
        
    @staticmethod
    def get_site_by_limit_offset(limit = 100, offset = 0):
        
        rss_site = RssSite()
        rss_sites = []
        cursor = rss_site.cursor(MySQLdb.cursors.DictCursor)
        try:
            
            cursor.execute("SELECT * FROM `rss_sites` LIMIT  %s , %s",
                           (offset * limit,  limit))
            
            sites = cursor.fetchall()
            for site in sites:
                 rss_sites.append(RssSite.new(site))
                 
            
        except MySQLdb.Error, e:
            logging.error("Insert entry Failed error : %s", e.args[1])
        
        finally:
            cursor.close()
        return rss_sites
        
        
    
    def _make_url_hash(self, url):
        """在python 3.0中 binasccicrc32() 返回范围  [0, 2**32-1] 
               此版本返回 范围  [-2**31, 2**31-1] 
        MySQL的CRC32也是 [0, 2**32-1] 
        """
        #使其返回正整数， 在python 2.7.3中
        return (crc32(url) & 0xFFFFFFFF)
        
    def update_md5(self, content_md5):
        
        cursor = self.cursor(MySQLdb.cursors.DictCursor)
        try:
            
            cursor.execute("UPDATE `rss_sites` SET `content_md5` = %s \
                            WHERE `url` = %s ",
                           (content_md5, self['url']))
            
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("update content md5 Failed error : %s", e.args[1])
            return False
        
        finally:
            cursor.close()
      
        return True
        
        
    
   
    
        
        
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
    
    @classmethod
    def find_by_url(cls, url):
        
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
        
        
    
    
    
    def _make_url_hash(self, url):
        """在python 3.0中 binasccicrc32() 返回范围  [0, 2**32-1] 
               此版本返回 范围  [-2**31, 2**31-1] 
        MySQL的CRC32也是 [0, 2**32-1] 
        """
        #使其返回正整数， 在python 2.7.3中
        return (crc32(url) & 0xFFFFFFFF)
        
    def _create(self, rss_entry):
        
        pass
        
    
    def _save(self):
        
        cursor = self.cursor()
        try:
            cursor.execute("INSERT INTO `rss_site_entries`(`id`, `site_url`, `title`, `author`, `link`, `description`, `entriy_md5`) \
                                    VALUE(NULL, %s, %s, %s, NULL, NULL, 0)",
                        (self['id'], self['site_url'], self['title'], self['author'], self['lnik'],self['description'], self.entry_md5 ))
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("Insert entry Failed error : %s", e.args[1])
            return False
        
        finally:
            cursor.close()
        
        return True
    
    
   
    
        
        
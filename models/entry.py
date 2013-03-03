#-*-coding:utf-8 -*-
#!/usr/bin/python


from model import Model
import hashlib
import MySQLdb
import logging

from time import  strftime, gmtime

class Entry(Model):
    
    def __init__(self):
        
        Model.__init__(self)
    
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
    
    
    @property
    def entry_md5(self):
        
        return hashlib.md5(self['title'] + self['description']).hexdigest()
    
        
        
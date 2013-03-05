#-*-coding:utf-8 -*-

from crawler.RssCrawler import *
import threading
import pprint

from models.model import Model
import Queue
from models.rsssite import RssSite
from models.entry import  Entry

from tornado.options import define, options

define("port", default = 8000, help  = "run on given port", type = int)
define("mysql_host", default = "localhost", help = "blog database host")
define("mysql_database", default = "rss_db", help = "rss server database name")
define("mysql_user", default = "thomas", help = "rss server database user")
define("mysql_password", default = "thomas", help="rss server database password")
define("mysql_port", default = 3036, help="rss server database port", type = int)


class RssMangerPool():
    """
    """
    @methodstaic
    def instance(thread_threshold = 5):
        if hasattr(RssMangerPool, "_instance", None) == None:
            RssMangerPool._instance = RssManagerPool(thread_threshold)
        return RssMangerPool._instance
     
    def __init__(self,thread_threshold = 5):  
        self.thread_threshold = thread_threshold
        self.tasks = Queue.Queue()
    
    def put_task(self, task):
        self.tasks.put(task)
    
    def get_task(self):
       return self.tasks.get()
    
    def run(self):
        for i in range(self.thread_threshold):
            thread_worker = threading.Thread(target=self.do_task)
            thread_worker.start()
            
    def do_task(self):
        while True:
            scrawler = self.get_task()
            if scrawler:
                scrawler.run()
        
    def update_site(self):
        pass
    
    

if __name__ == "__main__":
    
    db_settings = dict(
                               use_unicode = True, 
                                   charset = "utf8",
                                      host = options.mysql_host, 
                                        db = options.mysql_database,
                                     user  = options.mysql_user, 
                                    passwd = options.mysql_password,
                               )
    
    #site_url = "http://www.xiami.com/collect/feed"
    site_url = "http://feed.36kr.com/c/33346/f/566026/index.rss"
    Model.initailize(db_settings)
    
    #rss_site = RssSite.find_by_url(site_url)
    
    
    crawler = RssCrawler(site_url)
    
    for rss_entry in crawler.entries:
        
        entry = Entry.find_by_link(rss_entry.link)
        if entry.is_empty():
            
            Entry.create(rss_entry, site_url )
            
        elif entry.entry_md5 != rss_entry.entry_md5:
#            print "rss_link : %s" %(rss_entry.link)
#            print "link : %s" %(entry['link'])
#            print "entry_md5     : %s"  %(entry.entry_md5())
#            print "rss_entry_md5 : %s"  %(rss_entry.entry_md5())
#            entry['description'] = rss_entry.description
#            entry['title'] = rss_entry.title
#            print "After entry_md5 : %s"  %(entry.entry_md5())
             entry.save()
    
    print "\n Ok"
        
        
        
        
        


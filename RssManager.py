#-*-coding:utf-8 -*-

from crawler.RssCrawler import *
import threading
import time
from models.model import Model

import Queue
from models.rsssite import RssSite
from models.entry import Entry

from config.settings import *


class RssManagerPool():
    """limit : 设置每次获取更新网站的个数
        thread_threshold： 设置更新网站内容的线程工人数
        例子：
         db_settings = dict(
                               use_unicode = True, 
                                   charset = "utf8",
                                      host = options.mysql_host, 
                                        db = options.mysql_database,
                                     user  = options.mysql_user, 
                                    passwd = options.mysql_password,
                               )
    Model.initailize(db_settings)
    rss_manager = RssManagerPool.instance(5, 5)
    rss_manager.run()
    """

    @staticmethod
    def instance(thread_threshold=5, limit=5):
        if not hasattr(RssManagerPool, "_instance"):
            RssManagerPool._instance = RssManagerPool(thread_threshold, limit)
        return RssManagerPool._instance

    def __init__(self, thread_threshold, limit):
        self.query_limit = limit
        self.thread_threshold = thread_threshold
        self.tasks = Queue.Queue()

    def load_site(self):
        while True:
            site_count = RssSite.get_site_count()
            print "site count : %s" % (site_count)
            loops = site_count / self.query_limit + 1
            for i in range(loops):
                rss_sites = RssSite.get_site_by_limit_offset(self.query_limit, offset=i)
                for rss_site in rss_sites:
                    self.put_task(RssCrawler(rss_site))

            time.sleep(5 * 60)

    def put_task(self, task):
        self.tasks.put(task)

    def get_task(self):
        return self.tasks.get()

    def run(self):
        t = threading.Thread(target=self.load_site)
        t.daemon = True
        t.start()
        for i in range(self.thread_threshold):
            thread_worker = threading.Thread(target=self.do_task)
            thread_worker.start()

    def do_task(self):
        while True:
            scrawler = self.get_task()
            if scrawler:
                scrawler.run()


if __name__ == "__main__":
    """
    解决 UnicodeEncodeError: 'ascii' codec can't encode characters
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    """
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')

    db_settings = dict(
        use_unicode=True,
        charset="utf8",
        host=options.mysql_host,
        db=options.mysql_database,
        user=options.mysql_user,
        passwd=options.mysql_password,
    )
    Model.initailize(db_settings)
    rss_manager = RssManagerPool.instance(5, 5)
    rss_manager.run()
        
        
        
        


#-*-coding:utf-8 -*-

from crawler.RssCrawler import *

import pprint

from models.model import Model

from models.rsssite import RssSite

from tornado.options import define, options

define("port", default = 8000, help  = "run on given port", type = int)
define("mysql_host", default = "localhost", help = "blog database host")
define("mysql_database", default = "rss_db", help = "rss server database name")
define("mysql_user", default = "thomas", help = "rss server database user")
define("mysql_password", default = "thomas", help="rss server database password")
define("mysql_port", default = 3036, help="rss server database port", type = int)


if __name__ == "__main__":
    
    db_settings = dict(
                               use_unicode = True, 
                                   charset = "utf8",
                                      host = options.mysql_host, 
                                        db = options.mysql_database,
                                     user  = options.mysql_user, 
                                    passwd = options.mysql_password,
                               )
        
    Model.initailize(db_settings)
    
    rss_site = RssSite.find_by_url("http://www.xiami.com/collect/feed")
    
    pprint.pprint( rss_site._data)
    
#    crawler = RssCrawler("http://www.xiami.com/collect/feed")
#    
#    for entry in crawler.entries:
#        
#        print(entry)
#        
        
        
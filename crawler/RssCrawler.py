# -*- coding: utf-8 -*-

import feedparser
import hashlib
from models.entry import Entry

class RssCrawler:
    
    def __init__(self, rss_site):
        self.entries = []
        self.site_url = rss_site['url']
        feed = feedparser.parse(self.site_url)
        feed_md5 = hashlib.md5(str(feed)).hexdigest()
        if rss_site['content_md5'] !=  hashlib.md5(str(feed)).hexdigest():
            entries = feed.entries
            for entry in entries:
                self.add_entry(RssEntry(entry))
            rss_site.update_md5(feed_md5)
    
#    def __init__(self, feed):
#        """ 有些网站RSS聚集有重复的链接，但内容却不一样的
#        """
#        self.entries = []
#        entries = feed.entries
#        for entry in entries:
#            self.add_entry(RssEntry(entry))
        
    
    def add_entry(self, rss_entry):
       
        self.entries.append(rss_entry)
        
    
    def run(self):
        self.update_site_entry()
       
        
    def update_site_entry(self):
        for rss_entry in self.entries:
        
            entry = Entry.find_by_link(rss_entry.link)
            if entry.empty:
            
                Entry.create(rss_entry, self.site_url)
            
            elif entry.entry_md5 != rss_entry.entry_md5:
#               print "rss_link : %s" %(rss_entry.link)
#               print "link : %s" %(entry['link'])
#               print "entry_md5     : %s"  %(entry.entry_md5())
#               print "rss_entry_md5 : %s"  %(rss_entry.entry_md5())
                entry['description'] = rss_entry.description
                entry['title'] = rss_entry.title
#               print "After entry_md5 : %s"  %(entry.entry_md5())
                entry.save()
                
        

class RssEntry:
    
    
    def __init__(self, entry):
        
        self.entry = entry
        self.title = self._title()
        self.author = self._author()
        self.link = self._link()
        self.description = self._description()
        
    @property
    def entry_md5(self):
        return self._get_entry_md5()
    
    def _get_entry_md5(self):
        
        return hashlib.md5(self.title + self.description).hexdigest()
    
    def _description(self):
        
        description  = None
        if "content" in self.entry:
            description = self.entry.content[0].value
            
        elif "description" in self.entry:
            description = self.entry.description
        
        else:  
            description = self.entry.summary
        
        return description
    
    def _link(self):
        
        return self.entry.link
        
    def _title(self):
        
        return self.entry.title
    def _author(self):
        
        return self.entry.author
    
    def __str__(self):
        
        return """RssEntry : { 
      title : "%s",
       link : "%s",
     author : "%s",
description : 
  "%s", 
        md5 : "%s"
}\n""" %(self.title, self.link, self.author, self.description, self.entry_md5)




    
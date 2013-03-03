# -*- coding: utf-8 -*-

import feedparser
import hashlib


class RssCrawler:
    
    
    def __init__(self, url):
        
        self.entries = []
        feed = feedparser.parse(url)
        entries = feed.entries
        
        for entry in entries:
            self.add_entry(RssEntry(entry))
        
    
    def add_entry(self, rss_entry):
        self.entries.append(rss_entry)

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

    
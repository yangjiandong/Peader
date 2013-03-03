
from RssCrawler import *

import pprint


if __name__ == "__main__":
    
    
    crawler = RssCrawler("http://feed.luobo8.com/")
    
    
    for entry in crawler.entries:
        
        print(entry)
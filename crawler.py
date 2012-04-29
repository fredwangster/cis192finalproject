'''Scans url and retrieves domestic urls
    -returns list of domestic urls

    --parameters--
    url_name: the url to crawl
    crawl_depth: how many links to follow (recommended: 1 or 2)
    url_list: specify "[]". This will be list of urls obtained from the main page
    
'''

import urllib2
import time
import re

def crawler(url_name, crawl_depth, url_list):
    start = time.time()
    new_urls = []
    if crawl_depth > 0:
        #try:
        host = urllib2.urlopen(url_name)
        print "going through %s..." % url_name
        for line in host:
            #find urls
            urls = re.findall('<a href\s?=(\s?.+?)>',line)
            new_urls.extend(urls)

            for url in urls:
                print "found %s" % url
                
                #remove foreign urls
                
                if 'http' in url and not(url_name) in url:  
                    new_urls.remove(url)
                #recursively go through each url    
                else: 
                    url_list.append(crawler(url.strip("\""), crawl_depth-1, new_urls))
        #except:
         #   return []
    end = time.time()

    print "Crawled %s pages in %s seconds" % (len(url_list), start-end)
    return url_list
            
    
if __name__ == "__main__":
    crawler("http://www.amazon.com", 2, [])

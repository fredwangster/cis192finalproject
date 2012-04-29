'''Scans url and retrieves domestic urls
    -returns list of domestic urls

    --parameters--
    url_name: the url to crawl
    crawl_depth: how many links to follow (recommended: 1 or 2)
    url_list: specify "set()". This will be list of urls obtained from the main page
    
'''

import urllib2
import time
from sets import Set
from bs4 import BeautifulSoup
from urlparse import urljoin

def crawler(url_name, crawl_depth, url_set):
    start = time.time()
    new_urls = set()
    if crawl_depth > 0:
        #try:
        request = urllib2.Request(url_name)
        handle = urllib2.build_opener()
        print "going through %s..." % url_name
        content = unicode(handle.open(request).read(), "utf-8", errors="replace")
        soup = BeautifulSoup(content)

        temp_urls = set()
                          
        #find urls
        for link in soup.find_all('a'):
            raw_url = link.get('href')
            if raw_url is not None and not(raw_url in url_set):
                temp_urls.update(link.get('href'))
                new_urls.update(link.get('href'))
                          
        for url in temp_urls:
            print "found %s" % url
            #remove foreign urls...
            #not fool-proof. i.e. would remove amazon.com/http...
            #!!! Need future revision
            if 'http' in url and not(url_name) in url:
                print "removed the alien"
                new_urls.remove(url)
             
            #recursively go through each url:

            #case 1: no http found. need to append url_name
            elif not('http' in url):
                appended = urljoin(url_name, url)
                url_set.update(crawler(appended, crawl_depth-1, new_urls))
                
        #except:
         #   return []
    end = time.time()

    print "Crawled %s pages in %s seconds" % (len(url_list), end-start)
    return url_list
            
    
if __name__ == "__main__":
    print(crawler("http://www.gabrielweinberg.com", 2, set()))

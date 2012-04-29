'''Scans url and retrieves domestic urls
    -returns list of domestic urls

    --parameters--
    url_name: the url to crawl
    crawl_depth: how many links to follow (recommended: 1 or 2)
    url_list: specify "set()". This will be list of urls obtained from the main page
    
'''

import urllib2
import time
from bs4 import BeautifulSoup
from urlparse import urljoin

def crawler(url_name, crawl_depth, master_list):
    start = time.time()
    new_urls = []
    if crawl_depth > 0:
        #try:
        request = urllib2.Request(url_name)
        handle = urllib2.build_opener()
        print "going through %s..." % url_name
        content = unicode(handle.open(request).read(), "utf-8", errors="replace")
        soup = BeautifulSoup(content)
        temp_urls = []
                          
        #find urls
        for link in soup.find_all('a'):
            raw_url = link.get('href')
            if (raw_url is not None) and not(raw_url in master_list): \
               #and not(raw_url in temp_urls) and not(raw_url in new_urls):
                temp_urls.append(link.get('href'))
                new_urls.append(link.get('href'))
                          
        for url in temp_urls:
            print "found %s" % url
            #remove foreign urls...
            #not fool-proof. i.e. would remove amazon.com/http...
            #!!! Need future revision !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if 'http' in url and (url_name not in url):
                print "removed alien"
                new_urls.remove(url)
             
            #recursively go through each url:

            #case 1: no "http" found. need to append url_name
            elif not('http' in url):
                appended = urljoin(url_name, url)
                master_list.extend(crawler(appended, crawl_depth-1, new_urls))

            #case 2: url is perfect
            else:
                master_list.extend(crawler(url, crawl_depth-1, new_urls))
    
        #except:
         #   return []
    end = time.time()

    print "Crawled %s pages in %s seconds" % (len(master_list), end-start)
    return master_list
            
    
if __name__ == "__main__":
    print(crawler("http://www.gabrielweinberg.com", 2, []))

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
from urlparse import (urljoin, urlparse)

def crawler(root, url_name, crawl_depth, master_list):
    start = time.time()
    new_urls = []
    if crawl_depth > 0:
        print "crawling at depth: %s" %crawl_depth
        crawl_depth = crawl_depth - 1
        try:
            request = urllib2.Request(url_name)
            handle = urllib2.build_opener()
            print "going through %s..." % url_name
            content = unicode(handle.open(request).read(), "utf-8", errors="replace")
            soup = BeautifulSoup(content)
            temp_urls = []
                              
            #find urls
            raw_urls = soup.find_all('a')
            for link in soup.find_all('a'):
                raw_url = link.get('href')
                if (raw_url is not None) and not(raw_url in master_list)\
                   and not(raw_url in temp_urls) and not(raw_url in new_urls)\
                   and not(raw_url == ""):
                    temp_urls.append(raw_url)
                    new_urls.append(raw_url)
                              
            for url in temp_urls:
                #print "found %s" % url
                #remove foreign urls...
                #not fool-proof. i.e. would remove amazon.com/http...
                #!!! Need future revision !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                if 'http' in url and (root not in url):
                    #print "removed alien"
                    new_urls.remove(url)
                    #print new_urls

            #recursively go through each url:
            for url in new_urls:
                #case 1: no "http" found. need to append url_name
                print "crawling %s" % url
                if not('http' in url):
                    appended = urljoin(url_name, url)
                    #new_urls.extend(master_list)
                    master_list.extend(crawler(root, appended, crawl_depth, new_urls))

                #case 2: url is perfect
                else:
                    #new_urls.extend(master_list)
                    master_list.extend(crawler(root, url, crawl_depth, new_urls))
    
        except:
            return []
    end = time.time()
    print "Crawled %s pages in %s seconds" % (len(master_list), end-start) #print master_list

    seen = set()
    seen_add = seen.add
    return [ x for x in master_list if x not in seen and not seen_add(x)]
           
    
if __name__ == "__main__":
    a = []
    print(crawler("http://www.gabrielweinberg.com", "http://www.gabrielweinberg.com", 1, a))

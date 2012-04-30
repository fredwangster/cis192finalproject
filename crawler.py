'''Scans url and retrieves domestic urls
    -returns output file name, root url

    --parameters--
    root: the main url to crawl
    crawl_depth: how many levels to crawl (recommended: 2). Root is level 0

'''

import urllib2
import time
import os
#from sets import Set
from bs4 import BeautifulSoup
from urlparse import urljoin


class Crawler():
    def __init__(self):
        self.visited = []
        self.to_visit = set()
        self.to_add = set()
        self.to_remove = set()
        
    def crawler(self, root, crawl_depth):
        '''main crawler: iterates through every depth level
        calls helper function "scrape_urls" to find urls'''
       
        start = time.time()
        root_name = root.replace("/","").replace(":","")
        self.to_visit.add(root)
        while crawl_depth > 0:
            for site in self.to_visit:
                if site not in self.visited:
                    self.to_add.update(self.scrape_urls(root_name, site))
                    self.to_remove.add(site)
                    self.visited.append(site)

            self.to_visit.update(self.to_add)
            self.to_visit.difference_update(self.to_remove)
            print "Done depth: %s" %crawl_depth
            crawl_depth = crawl_depth - 1
        end = time.time()

        
        visit_list = list(self.to_visit)
        self.visited.extend(visit_list)

        print "Time elapsed: %s secs, URLS: %s links" % (end-start, len(self.visited))

       
        out_name = "./url_inputs/" +str(root_name[4:-1])+".txt"
        try:
            os.mkdir('./url_inputs')
            
        except:
            pass
        f = open(out_name, 'w')
        f.writelines(["%s\n" % item for item in self.visited])
        f.close()
            
        
        return out_name, root_name[4:]

    def scrape_urls(self, root, url_name):
        try:
            request = urllib2.Request(url_name)
            handle = urllib2.build_opener()
            print "scraping for urls -- %s" % url_name
            content = unicode(handle.open(request).read(), "utf-8", errors="replace")

            soup = BeautifulSoup(content)
            new_urls = set()

            #find urls
            #raw_urls = soup.find_all('a')
            for link in soup.find_all('a'):
                raw_url = link.get('href')
                if (raw_url is not None) and (raw_url != "") and (raw_url not in self.to_visit)\
                   and (raw_url not in self.visited):
                    #don't add foreign urls
                    if 'http' in raw_url and (root not in raw_url):
                        new_urls.add("")
                    elif not ('http' in raw_url):
                    #http isn't in file name (rel url), so we must create it ourselves
                        appended = urljoin(url_name, raw_url)
                        new_urls.add(appended)
                    else:
                        new_urls.add(raw_url)
        except:
            return set()

        return new_urls

if __name__ == "__main__":
    c = Crawler()
    print((c.crawler("http://www.imgur.com", 1)))

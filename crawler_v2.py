'''Scans url and retrieves domestic urls
    -returns list of domestic urls

    --parameters--
    url_name: the url to crawl
    crawl_depth: how many links to follow (recommended: 1 or 2)
    url_list: specify "set()". This will be list of urls obtained from the main page
    
'''

import re
import sys
import time
import math
import urllib2
from urlparse import (urlparse, urljoin)
import optparse
from cgi import escape
from traceback import format_exc
from Queue import Queue, Empty as QueueEmpty

from bs4 import BeautifulSoup

__version__ = "0.2"
__copyright__ = "CopyRight (C) 2008-2011 by James Mills"
__license__ = "MIT"
__author__ = "James Mills"
__author_email__ = "James Mills, James dot Mills st dotred dot com dot au"

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)


class Crawler(object):

    def __init__(self, root, depth, locked=True):
        self.root = root
        self.depth = depth
        self.locked = locked
        self.host = urlparse(root).geturl()
        self.urls = []
        self.links = 0
        self.followed = 0

    def crawl(self):
        page = Fetcher(self.root)
        page.fetch()
        q = Queue()
        for url in page.urls:
            q.put(url)
        followed = [self.root]

        n = 0

        while True:
            try:
                url = q.get()
            except QueueEmpty:
                break

            n += 1

            if url not in followed:
                try:
                    host = urlparse(url)[1]
                    if self.locked and re.match(".*%s" % self.host, host):
                        followed.append(url)
                        self.followed += 1
                        page = Fetcher(url)
                        page.fetch()
                        for i, url in enumerate(page):
                            if url not in self.urls:
                                self.links += 1
                                q.put(url)
                                self.urls.append(url)
                        if n > self.depth and self.depth > 0:
                            break
                except Exception, e:
                    print "ERROR: Can't process url '%s' (%s)" % (url, e)
                    print format_exc()
    def get_urls():
        return self.urls

class Fetcher(object):

    def __init__(self, url):
        self.url = url
        self.urls = []

    def __getitem__(self, x):
        return self.urls[x]

    def _addHeaders(self, request):
        request.add_header("User-Agent", AGENT)

    def open(self):
        url = self.url
        try:
            request = urllib2.Request(url)
            handle = urllib2.build_opener()
        except IOError:
            return None
        return (request, handle)

    def fetch(self):
        request, handle = self.open()
        self._addHeaders(request)
        if handle:
            try:
                content = unicode(handle.open(request).read(), "utf-8",
                        errors="replace")
                soup = BeautifulSoup(content)
                tags = soup.find_all('a')
            except urllib2.HTTPError, error:
                if error.code == 404:
                    print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
                else:
                    print >> sys.stderr, "ERROR: %s" % error
                tags = []
            except urllib2.URLError, error:
                print >> sys.stderr, "ERROR: %s" % error
                tags = []
            try:
                for tag in tags:
                    href = tag.get("href")
                    if href is not None:
                        url = urljoin(self.url, href)
                        if url not in self:
                            self.urls.append(url)
            except:
                print "nada"

def getLinks(url):
    page = Fetcher(url)
    page.fetch()
    for i, url in enumerate(page):
        print "%d. %s" % (i, url)
    
if __name__ == "__main__":
    crawler = Crawler("http://www.gabrielweinberg.com", 1)
    crawler.crawl()
    print crawler.get_urls()

import urllib2
import time
import threading
import string
import json
import urllib2

'''Scans the source of a site'''
class Analyzer():
    def __init__(self, filename, url_name):
        #threading.Thread.__init__(self)
        self.filename = filename
        self.site = url_name
        self.unique_visitors =0
        self.number_of_lines =0
        self.total_ads = 0
        self.ad_site_list = ["doubleclick","ad.yield","ad.google","ad.yahoo","ad.facebook","googlesyndication","msads","adchoices","ShareThis","ValueClick","AdBrite","Burst"]
        #self.APIKey = "176d39847432f9602f8002b35e294828"
        self.competeURLPart1 = "http://apps.compete.com/sites/"
        self.competeURLPart2 = "/trended/uv/?apikey=176d39847432f9602f8002b35e294828&latest=1"
        
    def getAds(self):
        #print "Running"
        start = time.time()
        total = 0
        try:
            f = open(self.filename,'r')
        except:
            return
        number_of_lines = 0
        for line in f.readlines():
            #print line
            number_of_lines =number_of_lines+1
            total= total+sum([line.count(ad) for ad in self.ad_site_list])
        f.close()
        
        print self.site[4:-1]
        #print "Number of Lines:", number_of_lines
        
        #print  "Number of Ads:", total
        #print "Analyzing Time: %s" % (time.time() - start)
        #self.getUniqueVisitors()
        self.number_of_lines = number_of_lines
        self.total_ads = total
        return total, number_of_lines
        
    def getUniqueVisitors(self):
        start = time.time()
        url =  self.competeURLPart1+self.site[4:-1]+self.competeURLPart2
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        
        self.unique_visitors = data["data"]["trends"]["uv"][0]["value"]
        #print "Unique Visitors: %s" % unique_visitors
        return self.unique_visitors
        
    def getScore(self):
        #print float(self.total_ads)/float(self.number_of_lines), self.unique_visitors
        score = float(self.total_ads)/float(self.number_of_lines) * self.unique_visitors/10000
        print score
        return score


import urllib2
import time
import threading
import string
import json
import urllib2

'''Scans the source of a site'''
class Analyzer(threading.Thread):
    def __init__(self, filename, url_name):
        #threading.Thread.__init__(self)
        self.filename = filename
        self.site = url_name
        self.ad_site_list = ["doubleclick","ad.yield","ad.google","ad.yahoo","ad.facebook"]
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
        self.getUniqueVisitors()
        print self.site, "Number of Lines:", number_of_lines, "Number of Ads:", total    
        print "Analyzing Time: %s" % (time.time() - start)
        return total, number_of_lines
        
    def getUniqueVisitors(self):
        start = time.time()
        url =  self.competeURLPart1+self.site[4:-1]+self.competeURLPart2
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        
        
        print data["data"]["trends"]["uv"][0]["value"]
        #print "Analyzing Time: %s" % (time.time() - start)
        
        
# if __name__ == "__main__":
    # a = Analyzer("./new_dir/000_httpwikia.com.txt","wiki")
    # a.start()

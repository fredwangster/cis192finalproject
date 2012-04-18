import urllib2
import time
import threading
import string

'''Scans the source of a site'''
class Analyzer(threading.Thread):
    def __init__(self, filename, url_name):
        threading.Thread.__init__(self)
        self.filename = filename
        self.site = url_name
        self.ad_site_list = ["doubleclick","ad.yield","ad.google","ad.yahoo","ad.facebook"]
    def run(self):
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
        print self.site, "Number of Lines:", number_of_lines, "Number of Ads:", total    
        #print "Elapsed Time: %s" % (time.time() - start)
        
# if __name__ == "__main__":
    # a = Analyzer("./new_dir/000_httpwikia.com.txt","wiki")
    # a.start()

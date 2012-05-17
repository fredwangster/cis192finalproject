import urllib2
import json


class Analyzer():
    '''Scans the source of a site'''
    def __init__(self, filename, url_name):
        '''Filename is source file for all the urls of a site
        These have to exist!'''
        #threading.Thread.__init__(self)
        self.filename = filename
        self.site = url_name
        self.unique_visitors = 0
        self.number_of_lines = 0
        self.total_ads = 0
        self.visits = 0
        self.ad_site_list = ["doubleclick", "ad.yield", "ad.google", \
        "ad.yahoo", "ad.facebook", "googlesyndication", "msads", \
        "adchoices", "ShareThis", "ValueClick", "AdBrite", "Burst"]
        #self.APIKey = "176d39847432f9602f8002b35e294828"
        self.competeURLPart1 = "http://apps.compete.com/sites/"
        self.competeURLPart2 = \
        "/trended/uv/?apikey=2a8fcf87616efc656bfd7022f1d122ef&latest=1"
        self.competeURLPart2b = \
        "/trended/uv/?apikey=ac4f760dd7ce4a81992b716d3d30cbca&latest=1"
        self.competeURLPart2vis = \
        "/trended/vis/?apikey=2a8fcf87616efc656bfd7022f1d122ef&latest=1"
        self.competeURLPart2bvis = \
        "/trended/vis/?apikey=43a79f6cc67e7fcf0de42ae1e6f8cb76&latest=1"

    def getAds(self):
        '''Iterates through the urls in the filename and finds ads'''
        #print "Running"
        #start = time.time()
        total = 0
        number_of_lines = 0
        try:
            openfile = open(self.filename, 'r')
            for line in openfile.readlines():
                if line is not None and line != "":
                    #print line
                    try:
                        site = urllib2.urlopen(line)
                        for eachline in site:
                            number_of_lines = number_of_lines + 1
                            total = total + sum([eachline.count(ad) for ad \
                                                in self.ad_site_list])
                    except:
                        pass
            openfile.close()
        except:
            return
        
        
        #print self.site[4:-1]
        #print "Number of Lines:", number_of_lines
        #print  "Number of Ads:", total
        #print "Analyzing Time: %s" % (time.time() - start)
        self.getUniqueVisitors()
        if number_of_lines != 0:
            self.number_of_lines = number_of_lines
        else:
            self.number_of_lines = .01
        self.total_ads = total
        #print self.total_ads
        return total, number_of_lines

    def getUniqueVisitors(self):
        '''Pulls data from compete api on site visitors'''
        url =  self.competeURLPart1 + self.site[0:-1] \
              + self.competeURLPart2
        try:
            json_string = urllib2.urlopen(url).read()
        except:
            url =  self.competeURLPart1 + self.site[0:-1] \
                  + self.competeURLPart2b
            try:      
                json_string = urllib2.urlopen(url).read()
            except:
                print "-----------------------------------------------------"
                print "ERROR: You are out of Compete API Queries 2000 per day"
                print "-----------------------------------------------------"
                return
        data = json.loads(json_string)
        try:
            self.unique_visitors = data["data"]["trends"]["uv"][0]["value"]
        except:
            self.unique_visitors = 0
        #print "Unique Visitors: %s" % self.unique_visitors
        return self.unique_visitors

    def getVisits(self):
        '''Pulls data from compete api on site visits'''
        url =  self.competeURLPart1 + self.site[0:-1] \
              + self.competeURLPart2vis
        try:
            json_string = urllib2.urlopen(url).read()
        except:
            url =  self.competeURLPart1 + self.site[0:-1] \
                  + self.competeURLPart2bvis
            try:      
                json_string = urllib2.urlopen(url).read()
            except:
                print "-----------------------------------------------------"
                print "ERROR: You are out of Compete API Queries 2000 per day"
                print "-----------------------------------------------------"
                return
        data = json.loads(json_string)
        try:
            self.visits = data["data"]["trends"]["vis"][0]["value"]
        except:
            self.visits = .01
        #print "Unique Visitors: %s" % unique_visitors
        return self.visits

    def getScore(self):
        '''Calculates score based on our formulas
        for ads, % ads, and retention'''
        hasAds = 0
        if self.total_ads > 0:
            hasAds = 35
        percent_ad = 15 * float(self.total_ads) / float(self.number_of_lines)
        retention_score = 50 - 50 * abs(.15 - float(self.unique_visitors) \
                                        / self.visits)
        score = hasAds + percent_ad + retention_score
        return score

if __name__ == "__main__":
    a = Analyzer("./url_inputs/www.amazon.co.txt", "www.amazon.com/")
    a.getAds()

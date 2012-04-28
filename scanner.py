import urllib2
import time
import os
from analyzer import Analyzer
'''Scans the source of a site'''
def scanner(url_list, unique_code):
    print "Running"
    
    i =1
    for url in url_list:
            #print i,": ", url
            start = time.time()
            try:
                host  = urllib2.urlopen(url)
            except:
                #print "Error"
                #print '--------------------------------'
                continue
            url_name = url.replace("/","").replace(":","")
            try:
                os.mkdir('./output_files')
            except:
                pass
            html_name = "./output_files/" + unique_code+"_"+str(url_name[0:-1])+".txt"
            if not os.path.isfile(html_name):  
                f = open(html_name, 'w')
                f.write(host.read())
                f.close()
            a = Analyzer(html_name, url_name)
            a.getAds()
            i=1+i
            #print '--------------------------------'
            print "This Url's Total Time: %s" % (time.time() - start)
    raw_input("press any key to exit")
    
if __name__ == "__main__":
    f = open("top_sites.txt",'r')
    da_list = f.readlines()
    scanner(da_list, "000")


import urllib2
import time

'''Scans the source of a site'''
def scanner(url_list, unique_code):
    print "Running"
    start = time.time()
    for url in url_list:
            host  = urllib2.urlopen(url)
            url_name = url.replace("/","").replace(":","")
            html_name = unique_code+"_"+url_name+".txt"
            f = open(html_name, 'r+')
            f.write(host.read())
            f.close()
            
    print "Elapsed Time: %s" % (time.time() - start)
    raw_input("press any key to exit")
    
if __name__ == "__main__":

    da_list = ["http://yahoo.com", "http://google.com", "http://amazon.com",
      "http://ibm.com", "http://apple.com"]
    scanner(da_list, "000")


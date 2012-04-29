import urllib2
import time
import os
from analyzer import Analyzer

'''Scans the source of a site'''
def scanner(url, unique_code):
 
        #print i,": ", url
        start = time.time()
        try:
            host  = urllib2.urlopen(url)
        except:
            return
        url_name = url.replace("/","").replace(":","")
        try:
            os.mkdir('./output_files')
        except:
            pass
        
        html_name = "./output_files/" +str(url_name[4:-1])+".txt"
        
        if not os.path.isfile(html_name):  
            f = open(html_name, 'w')
            f.write(host.read())
            f.close()
        return html_name,url_name
    


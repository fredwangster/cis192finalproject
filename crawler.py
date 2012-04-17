import urllib2
import time

'''Scans scraped source and retrieves domestic urls'''
def crawler(url_list, unique_code):
    start = time.time()
    for url in url_list:
        url_name = url.replace("/","").replace(":","")
        html_name = unique_code+"_"+url_name+".txt"
        for line in open(html_name):
            

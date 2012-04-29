import urllib2
import time

'''Scans scraped source and retrieves domestic urls'''
def crawler(url_name, crawl_depth, url_list):
    start = time.time()
    dir_name = './output_files'
    new_urls = []
    
    if crawl_depth > 0:
        try:
            host = urllib2.urlopen(url)
            for line in host:
                #find urls
                urls = re.findall('?<a href\s?=\s?.+?>',line)
                new_urls.append(urls)
                
                for url in urls:
                    #remove foreign urls
                    if 'http' in url and not(url_name) in url:  
                        new_urls.remove(url)

                    
                    #recursively go through each url
                    url_list.append(crawler(url, crawl_depth-1, new_urls))
        except:
            return

    return url_list
            
    

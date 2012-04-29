1. get_top100k.py -> goes through the alexa top 1m list to get top 100k

2. scraper.py -> goes through specified list of site(s) to grab html
3. **crawler.py -> goes through list of html files to grab urls, then scrapes those urls, then crawls more
		 - (user-specified depth)
		 - should only grab urls within same domain

4. analyzer.py -> goes through html to measure advertisement
		- this is pretty discretionary for us... maybe just find the % google adsense lines to total non-javascript lines (i.e. content)? 

5. aggregator.py -> basically links scraper, crawler, and analyzer.
		- sends scraper to a list of urls
		- then sends crawler crawl depth to iterate through
		- after gathering all the html needed, run the analyzer on list of html
		- spit out analyzer output for each site
		- this should keep track of which urls are associated to each site

5. index.html -> lets user input list of urls 
		- sends these through to the aggregator.py backend
 		- spits out what the aggregator outputs.

 
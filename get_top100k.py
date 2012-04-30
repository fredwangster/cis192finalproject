import fileinput
from itertools import islice
f = open('top_sites.txt','w')

n = 100
nlines=0
for line in open("top_sites_long.txt"):
        f.write(line)
        nlines += 1
        if nlines >= n:
            break
f.close()

    

import fileinput
from itertools import islice
f = open('100k.csv','w')

n = 100000
nlines=0
for line in open("top-1m_list.csv"):
        f.write(line)
        nlines += 1
        if nlines >= n:
            break
f.close()

    

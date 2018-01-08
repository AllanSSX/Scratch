#!/usr/bin/env python

import sys
import gzip

count=0
with gzip.open(sys.argv[1],'r') as files:
	for line in files:
		if not (line.startswith (">")) :
			count+=  sum(1 for c in line if c.isupper())
	
print 'There are '+str(count)+' uppercase letters.'


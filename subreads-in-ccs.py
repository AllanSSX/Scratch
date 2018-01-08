#!/usr/bin/env python
# -*- coding: utf-8 -*-

#________________________________________________________________________________________________________________________________#

import argparse

#________________________________________________________________________________________________________________________________#

def getArgs():
	parser = argparse.ArgumentParser(description="",version="1.0")
	parser.add_argument('-c',dest="ccs",type=argparse.FileType('r'),required=True,help="Fastq ccs file")
	parser.add_argument('-s',dest="subreads",type=argparse.FileType('r'),required=True,help="Fastq subreads file")
	parser.add_argument('-o',dest="out",type=str,required=True,help="ID of ccs like subreads")
	
	arg = parser.parse_args()
	
	return arg

def main(arg):
	
	ccs_id = set()
	
	i=0
	for line in arg.ccs:
		if i % 4 == 0:
			ccs_id.add(line[:-4])
		i+=1
		
	ccs_like=open(arg.out, 'w')
	
	i=0
	for line in arg.subreads:
		if i % 4 == 0:
			subread_id = line.split('/')[0]+'/'+line.split('/')[1]+'/'
			if subread_id in ccs_id:
				ccs_like.write(line[1:-1]+'\n')
		i+=1
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

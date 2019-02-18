#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#________________________________________________________________________________________________________________________________#

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-i',dest="frags", type=argparse.FileType('r'),required=True,help='info_frags')
	parser.add_argument('-c',dest="sctg2chr", type=argparse.FileType('r'),required=True,help='sctg2chr')
	
	args = parser.parse_args()
	
	return args

def main(args):
	
	CHR = {}
	
	for line in args.sctg2chr:
		sctg, chr = line.split()
		CHR[sctg] = chr
		
	
	HiC = {}
	
	for line in args.frags:
		if line.startswith('>'):
			print(line[:-1])
			current = line.split()[0]
			HiC[current] = [[], []]
			
		elif not line.startswith('init'):
			sctg = line.split()[0]
			chr = CHR[sctg]
			orientation = line.split()[2]
			if not sctg in HiC[current][1]:
				HiC[current][1].append(sctg)
				print('\t'+chr+'\t'+orientation+'\t'+sctg)
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

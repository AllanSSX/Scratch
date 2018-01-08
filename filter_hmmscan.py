#!/usr/bin/env python
# -*- coding: utf-8 -*-

#________________________________________________________________________________________________________________________________#

import argparse
import sys

#________________________________________________________________________________________________________________________________#

def getArgs():
	parser = argparse.ArgumentParser(description="Filter hmmscan output file -> 1e-3 + formatting")
	parser.add_argument('-m',dest="hmmscan", type=argparse.FileType('r'),required=True,help='hmmscan output file')
	parser.add_argument('-f',dest="fasta", type=argparse.FileType('r'),required=True,help='input fasta file')
	
	
	args = parser.parse_args()
	
	return args

def main(args):
		
	prot = {}
	
	for line in args.fasta:
		if line.startswith('>'):
			prot[line.split()[0][1:]] = ''
	
	for line in args.hmmscan:
		if not line.startswith('#'):
			elem = line.split()
			seq = elem[2]
			pfam = elem[1]
			evalueDomain = float(elem[7])
		
			if evalueDomain < 0.001:
				if len(prot[seq]) == 2:
					prot[seq][0].append(pfam)
					prot[seq][1].append(' '.join(elem[18:]))
				else:
					prot[seq]=[[pfam] ,[' '.join(elem[18:])]]
					
	for key, value in sorted(prot.items()):
		if len(value) == 2:
			print(key+'\t'+','.join(value[0])+'\t'+','.join(value[1]))
		else:
			print(key)
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

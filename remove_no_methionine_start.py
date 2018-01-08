#!/usr/bin/env python

#________________________________________________________________________________________________________________________________#

import argparse
import sys

#________________________________________________________________________________________________________________________________#

def getArgs():
	parser = argparse.ArgumentParser(description="Remove non methionine proteins")
	parser.add_argument('-f',dest="fasta", type=argparse.FileType('r'),required=True,help='fasta file')
	
	args = parser.parse_args()
	
	return args

def main(args):
	
	prot = {}
	
	for line in args.fasta:
		if line.startswith('>'):
			if not prot:
				id = line[1:-1]
				seq = ''
				prot[id] = seq
			else:
				prot[id] = seq
				id = line[1:-1]
				seq = ''
		else:
			seq += line[:-1]
	
	for id, seq in prot.items():
		if seq.startswith('M'):
			print('>'+id)
			print(seq)
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

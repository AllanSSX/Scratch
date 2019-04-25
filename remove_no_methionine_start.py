#!/usr/bin/env python

#________________________________________________________________________________________________________________________________#

import argparse
import sys

#________________________________________________________________________________________________________________________________#

def getArgs():
	parser = argparse.ArgumentParser(description="Remove non methionine proteins")
	# parser.add_argument('-f',dest="fasta", type=argparse.FileType('r'),required=True,help='fasta file')
	parser.add_argument('-f',dest="fasta", type=str,required=True,help='fasta file')
	
	args = parser.parse_args()
	
	return args

def main(args):
	
	prot = {}
	
	reading = open(args.fasta, 'r')
	for line in reading.readlines():
		if line.startswith('>'):
			id = line[1:-1]
			seq = ''
			if not id in prot:
				prot[id] = seq
			else:
				print('Duplicate value for gene: '+id)
		else:
			prot[id] = prot[id] + line[:-1]
	
	good=open(args.fasta+'.good', 'w')
	bad=open(args.fasta+'.bad', 'w')
	
	for id, seq in prot.items():
		if seq.startswith('M'):
			good.write('>'+id+'\n')
			good.write(seq+'\n')
		else:
			bad.write('>'+id+'\n')
			bad.write(seq+'\n')
			
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

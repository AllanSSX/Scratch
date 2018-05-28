#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-b',dest="busco",type=argparse.FileType('r'),required=True, help='BUSCO full output file')
	parser.add_argument('-c',dest="coverage",type=argparse.FileType('r'),required=True, help='Coverage file')
	parser.add_argument('-g',dest="gc", type=argparse.FileType('r'), required=True, help='Print %GC for each sequence')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	gcCov = {}
	infos = {}
	
	for line in args.gc:
		contig, gc = line.split()
		gcCov[contig] = [gc]
		
	for line in args.coverage:
		if not line.startswith('#'):
			contig, reads, cov = line.split()
			if contig in gcCov:
				gcCov[contig].append(cov)
	
	for line in args.busco:
		if not line.startswith('#'):
			try:
				id, status, contig, start, end, score, length = line.split()
			except:
				id, status = line.split()
		
			if status == 'Missing':
				print('\t'.join([id, status]))
			else:
				gc = str(round(float(gcCov[contig][0]), 2))
				coverage = str(round(float(gcCov[contig][1]), 2))
				print('\t'.join([id, status, contig, gc, coverage]))
			
				
if __name__ == '__main__':
	args = getArgs()
	main(args)
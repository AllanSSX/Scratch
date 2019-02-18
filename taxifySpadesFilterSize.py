#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-t',dest="taxify",type=argparse.FileType('r'),required=True,help='taxify file for SPADES assembly')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	for line in args.taxify:
		seq, tax, score = line.split()
		NODE, nodeID, length, lgth, cov, coverage = seq.split('_')
		if int(lgth) >= 500:
			print(line[:-1])

if __name__ == '__main__':
	args = getArgs()
	main(args)
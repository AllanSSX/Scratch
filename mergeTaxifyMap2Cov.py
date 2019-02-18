#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-t',dest="taxs",type=argparse.FileType('r'),required=True,help='taxs file from taxify.py')
	parser.add_argument('-c',dest="cov",type=argparse.FileType('r'),required=True,help='coverage file from map2cov')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	coverage = {}
	
	for line in args.cov:
		if not line.startswith("#"):
			contig_id, read_cov, base_cov = line.split()
			coverage[contig_id] = base_cov
	
	print 'contig_id\tlength\tgc\tcoverage\ttax'
	for line in args.taxs:
		if not line.startswith("#"):
			contig_id, length, gc, taxonomy = line.split("\t")
			final_tax = taxonomy.split("=")[2].split(":")[0]
			if len(final_tax.split()) > 1:
				final_tax = final_tax.replace(" ","_")
			
			print contig_id+'\t'+length+'\t'+gc+'\t'+coverage[contig_id]+'\t'+final_tax
			
			


if __name__ == '__main__':
	args = getArgs()
	main(args)
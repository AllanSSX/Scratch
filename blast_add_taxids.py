#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-d',dest="diamond",type=argparse.FileType('r'),required=True,help='Diamond output (TSV)')
	parser.add_argument('-t',dest="taxids",type=str,required=True,help='accession2taxid')
	parser.add_argument('--diamond_taxids',action="store_true",help='Diamond accession2taxid format')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	blast = {}
	
	for line in args.diamond:
		subject = line.split()[1]
		if subject not in blast:
			blast[subject] = []
			blast[subject].append(line.split())
		else:
			blast[subject].append(line.split())		
	
	for line in open(args.taxids):
		if args.diamond_taxids:
			accession,taxid = line.split()
		else:
			prot,accession,taxid,gi = line.split()
		
		if accession in blast:
			for value in blast[accession]:
				print '\t'.join(value) + '\t' + taxid


if __name__ == '__main__':
	args = getArgs()
	main(args)
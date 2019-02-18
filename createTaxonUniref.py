#!/usr/bin/env python

import argparse
import re

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-u',dest="uniref",type=argparse.FileType('r'),required=True,help='Uniref fasta file with full header')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	for line in args.uniref:
		if line.startswith('>'):
			seqid = line.split()[0][1:]
			
			try:
				taxid = int(re.split('TaxID=', line)[1].split()[0])
				print(seqid+'\t'+str(taxid))
			except:
				pass
		
if __name__ == '__main__':
	args = getArgs()
	main(args)

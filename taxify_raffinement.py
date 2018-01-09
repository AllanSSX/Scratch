#!/usr/bin/env python

import argparse
import re

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-k',dest="kingdom",type=argparse.FileType('r'),required=True,help='Taxify kingdom file')
	parser.add_argument('-p',dest="phylum",type=argparse.FileType('r'),required=True,help='Taxify phylum file')
	parser.add_argument('-s',dest="specie",type=argparse.FileType('r'),required=True,help='Taxify specie file')
	parser.add_argument('-b',dest="busco",type=argparse.FileType('r'),required=True,help='BUSCO scaffolds list')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	specie = {}
	kingdom = {}
	BUSCO = {}
	
	for line in args.busco:
		BUSCO[line.split()[0]] = None
	
	for line in args.kingdom:
		seq, reads, cov, size, gc, taxo = line.split()
		if re.split('=|;', taxo)[3].split(':')[0] == 'Fungi':
			kingdom[seq] = None
	
	for line in args.specie:
		seq, reads, cov, size, gc, taxo = line.split()
		if (re.split('=|;', taxo)[3].split(':')[0]).startswith('Papilio'):
			specie[seq] = None
	
	for line in args.phylum:
		seq, reads, cov, size, gc, taxo = line.split()
		if re.split('=|;', taxo)[3].split(':')[0] == 'Microsporidia':
			print(line[:-1]+'\tL1')
		
		elif seq in specie:
			print(line[:-1]+'\tL2')
		elif seq in kingdom:
			print(line[:-1]+'\tL3')
		elif seq in BUSCO:
			print(line[:-1]+'\tL4')
			
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

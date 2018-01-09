#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="genome",type=str,required=True,help='genome')
	parser.add_argument('-m',dest="min",type=int,help='Min. seq. length')
	parser.add_argument('-M',dest="max",type=int,help='Max. seq. length')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	min = 0
	if args.min:
		min = args.min
	max = 100000000000000
	if args.max:
		max = args.max
	
	if min > max:
		print('Error, min > max')
		exit(1)
	
	genome_fasta = open('filter.fasta', 'w')
	for seq in SeqIO.parse(args.genome, "fasta"):	
		if len(seq.seq) >= min and len(seq.seq) <= max:
			genome_fasta.write('>'+seq.id+'\n')
			sequence = str(seq.seq)
			while len(sequence) > 0:
				genome_fasta.write(sequence[:70]+'\n')
				sequence = sequence[70:]
				
	genome_fasta.close()

if __name__ == '__main__':
	args = getArgs()
	main(args)

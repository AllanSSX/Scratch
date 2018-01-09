#!/usr/bin/env python

import argparse
import os
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	max_len = 0
	for fasta in SeqIO.parse(args.fasta, "fasta"):
		if len(fasta) > max_len:
			max_len = len(fasta)
			name = fasta.id
			sequence = str(fasta.seq)

	cluster = os.path.splitext(os.path.basename(args.fasta))[0]
	print('>'+cluster+'|'+name)
	while len(sequence) > 0:
		print(sequence[:70])
		sequence = sequence[70:]

if __name__ == '__main__':
	args = getArgs()
	main(args)


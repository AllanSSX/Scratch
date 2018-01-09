#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	for fasta in SeqIO.parse(args.fasta, "fasta"):
		name = fasta.id
		sequence = str(fasta.seq)
		singleFasta = open(name+'.fasta','w')
		singleFasta.write('>'+name+'\n')
		while len(sequence) > 0:
			singleFasta.write(sequence[:70]+'\n')
			sequence = sequence[70:]
		singleFasta.close()

if __name__ == '__main__':
	args = getArgs()
	main(args)
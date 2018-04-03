#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="ids",type=argparse.FileType('r'),required=True,help='old ids - new ids')
	parser.add_argument('-p',dest="protein",type=str,required=True,help='protein file')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	renaming = {}
	
	for line in args.ids:
		old, new = line.split()
		renaming[old] = new

	prot_fasta = open('protein.faa', 'w')
	
	for seq in SeqIO.parse(args.protein, "fasta"):
		if seq.id.split('.')[0] in renaming:
			name = (renaming[seq.id.split('.')[0]])
			prot_fasta.write('>'+name+'\n')
			sequence = str(seq.seq)
			while len(sequence) > 0:
				prot_fasta.write(sequence[:70]+'\n')
				sequence = sequence[70:]

if __name__ == '__main__':
	args = getArgs()
	main(args)

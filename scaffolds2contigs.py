#!/usr/bin/env python

import argparse
from Bio import SeqIO
import re


def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-i',dest="input",type=argparse.FileType('r'),required=True,help='Input fasta')
	# parser.add_argument('-o',dest="output",type=str,required=True,help='Output fasta')
	parser.add_argument('-g',dest="gap",type=int,required=True,help='Number of Ns for a gap from which seq. is splitted')
	parser.add_argument('-s',dest="size",type=int,required=True,help='Min contig size to print')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	for seq in SeqIO.parse(args.input, "fasta"):
		
		regex = '[nN]{'+str(args.gap)+',}'
		
		substring = re.sub(regex,'\n',str(seq.seq)).split('\n')
		i = 1
		for contig in substring:
			if len(contig) >= args.size :
				print('>'+seq.id+'_contig_'+str(i))
				i += 1
				sequence = str(contig)
				while len(sequence) > 0:
					print(sequence[:70])
					sequence = sequence[70:]

if __name__ == '__main__':
	args = getArgs()
	main(args)

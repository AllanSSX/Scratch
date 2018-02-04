#!/usr/bin/env python

import argparse
from Bio import SeqIO
import re

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-g',dest="gtf",type=argparse.FileType('r'),required=True,help='GTF from GeneMark ES')
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='Protein fasta file from GeneMark ES')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	id2sctg = {}
	
	for line in args.gtf:
		sctg, source, feature, start, end, score, strand, frame, attribute_1,  attribute_2, attribute_3, attribute_4 = line.split()
		attribute_2 = re.sub('"|;','', attribute_2)
		# print(sctg, re.sub('"|;','', attribute_2))
		if attribute_2 not in id2sctg:
			id2sctg[attribute_2] = [sctg, attribute_2.split('_')[0]]

	for seq in SeqIO.parse(args.fasta, "fasta"):
		
		# print(seq.id, id2sctg[seq.id])
		
		print('>'+'_'.join(id2sctg[seq.id]))
		sequence = str(seq.seq)
		while len(sequence) > 0:
			print(sequence[:70])
			sequence = sequence[70:]


			
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

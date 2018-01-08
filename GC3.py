#!/usr/bin/env python3

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="Compute GC3 for each sequence (/!\ uppercase fasta)")
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='fasta (cds)')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	gc3 = {}
	
	for seq in SeqIO.parse(args.fasta, "fasta"):
		
		gc3[seq.id]= {'A': 0, 'T': 0, 'C' : 0, 'G': 0}
		sequence = str(seq.seq)
		for codon in range(2, len(sequence), 3):
			base = sequence[codon]
			if base in gc3[seq.id]:
				gc3[seq.id][base] += 1
	
	
	for gene, bases in sorted(gc3.items()):
		gc3 = round((bases['G'] + bases['C']) / (bases['A'] + bases['T'] + bases['C'] + bases['G']), 2)
		print(gene+'\t'+str(bases['A'])+'\t'+str(bases['T'])+'\t'+str(bases['C'])+'\t'+str(bases['G'])+'\t'+str(gc3))


if __name__ == '__main__':
	args = getArgs()
	main(args)

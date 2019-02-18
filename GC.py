#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='fasta')
	parser.add_argument('-d',dest="detail", action='store_true', help='Print GC for each sequence')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	nuclFasta = {'A':0, 'a':0,'C':0, 'c':0,'G':0, 'g':0,'T':0, 't':0,'N':0, 'n':0}
	for seq in SeqIO.parse(args.fasta, "fasta"):
		
		nucl = {'A':0, 'a':0,'C':0, 'c':0,'G':0, 'g':0,'T':0, 't':0,'N':0, 'n':0}
		sequence = str(seq.seq)
		for codon in sequence:
			if codon in nucl:
				nucl[codon] += 1
				nuclFasta[codon] += 1
				
		A = nucl['A'] + nucl['a']; C = nucl['C'] + nucl['c']; G = nucl['G'] + nucl['g']; T = nucl['T'] + nucl['t']; N = nucl['N'] + nucl['n']
		size = A + G + C + T		
		GC = float((G + C)) / float(size) * 100
		if args.detail:
			print(str(seq.id)+'\t'+str(GC))
	
	A = nuclFasta['A'] + nuclFasta['a']; C = nuclFasta['C'] + nuclFasta['c']; G = nuclFasta['G'] + nuclFasta['g']; T = nuclFasta['T'] + nuclFasta['t']
	size = A + G + C + T		
	GC = float((G + C)) / float(size) * 100
	print('Global GC value:' + str(round(GC,2)))

if __name__ == '__main__':
	args = getArgs()
	main(args)

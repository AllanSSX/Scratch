#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="Correction of ##sequence-region tag")
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='Genome')
	parser.add_argument('-g',dest="gff",type=argparse.FileType('r'),required=True,help='gff3')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	dictSeq = {}
	
	for seq in SeqIO.parse(args.fasta, "fasta"):
		dictSeq[seq.id] = len(seq.seq)

	gff3 = open('output.gff3', 'w')
	for line in args.gff:
		if line.startswith('##sequence'):
			tag, scaffold, start, end = line.split()
			start = 1
			end = dictSeq[scaffold]
			
			gff3.write(tag+'   '+scaffold+' '+str(start)+' '+str(end)+'\n')
			
		else:
			gff3.write(line)
			

if __name__ == '__main__':
	args = getArgs()
	main(args)

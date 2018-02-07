#!/usr/bin/env python

import argparse
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from BCBio import GFF

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='Input fasta')
	parser.add_argument('-g',dest="gff",type=str,required=True,help='Input gff3')
	parser.add_argument('-o',dest="output",type=str,required=True,help='Output name')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	output = open(args.output+".gb", "w")
	sequences = SeqIO.to_dict(SeqIO.parse(args.fasta, "fasta", generic_dna))
	gff_iter = GFF.parse(args.gff, sequences)
	SeqIO.write(gff_iter, output, "genbank")	


if __name__ == '__main__':
	args = getArgs()
	main(args)

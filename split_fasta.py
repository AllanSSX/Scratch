#!/usr/bin/env python

import argparse
import sys
from Bio import SeqIO
from Bio.SeqIO.FastaIO import FastaWriter

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	for fasta in SeqIO.parse(args.fasta, "fasta"):

		out = open(fasta.id+".fasta", "w")
		
		fasta_out = FastaWriter(out, wrap=70)
		fasta_out.write_header()
		fasta_out.write_record(fasta)
		
		out.close()

if __name__ == '__main__':
	args = getArgs()
	main(args)
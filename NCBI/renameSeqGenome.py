#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="Rename sequences ID from a fasta file. Seq will be sorted by size (decreasing)")
	parser.add_argument('-f',dest="genome",type=str,required=True,help='genome')
	parser.add_argument('-p',dest="prefix",type=str,required=True,help='Prefix for the seq. name')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	old2new = {}
	dictSeqLen = {}
	dictSeq = {}
	
	for seq in SeqIO.parse(args.genome, "fasta"):
		
		dictSeq[seq.id] = str(seq.seq)
		dictSeqLen[seq.id] = len(seq.seq)
		
	sortedSeqByLgth = []
	sortedSeqByLgth = sorted(dictSeqLen,key=dictSeqLen.get,reverse=True)
	
	prefix = args.prefix
	suffix = 1
	
	for i in sortedSeqByLgth:
		chr = prefix + str(format(suffix, '06d'))
		print('>'+ chr)
		sequence = dictSeq[i]
		while len(sequence) > 0:
			print(sequence[:70])
			sequence = sequence[70:]
		
		old2new[i] = chr
		suffix += 1
	
	####
	
	genome_updated = open('updated.seqID', 'w')
	
	for key, value in sorted(old2new.items()):
		genome_updated.write(key+'\t'+value+'\n')
	
	genome_updated.close()
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

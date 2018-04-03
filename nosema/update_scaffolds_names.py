#!/usr/bin/env python

import argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="genome",type=str,required=True,help='genome')
	
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
	
	prefix = 'NGRA'
	suffix = 10000
	
	genome_fasta = open('updated.fasta', 'w')
	
	for i in sortedSeqByLgth:
		chr = prefix + str(format(suffix, '06d'))
		genome_fasta.write('>'+ chr + '\n')#' length=' + str(dictSeqLen[i]) + '\n')# + ' organism=Nosema granulosis\n')
		sequence = dictSeq[i]
		while len(sequence) > 0:
			genome_fasta.write(sequence[:70]+'\n')
			sequence = sequence[70:]
		
		old2new[i] = chr
		suffix += 1
	
	genome_fasta.close()
	
	####
	
	genome_updated = open('updated.names', 'w')
	
	for key, value in sorted(old2new.items()):
		genome_updated.write(key+'\t'+value+'\n')
	
	genome_updated.close()
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

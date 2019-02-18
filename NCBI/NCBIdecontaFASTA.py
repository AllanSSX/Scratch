#!/usr/bin/env python

import argparse
import re
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="Trim fasta file from NCBI Contamination.txt file")
	parser.add_argument('-f',dest="genome",type=str,required=True,help='genome')
	parser.add_argument('-t',dest="trim",type=argparse.FileType('r'),required=True,help='Trimming part: <sequence> <length> <span(s)> <source>')
	parser.add_argument('-r',dest="remove",type=argparse.FileType('r'),required=True,help='List of contigs to remove')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	remove = {}
	for line in args.remove:
		remove[line.split()[0]] = None
	
	trim = {}
	for line in args.trim:
		sequence, length, span, source = line.split()
		trim[sequence] = []
		for bloc in span.split(','):
			trim[sequence].append(re.split('\.\.', bloc))
			# trim[sequence] = trim[sequence] + re.split('\.\.', bloc)
		# print(trim[sequence])
	
	dictSeq = {}
	dictSeqLen = {}
	for seq in SeqIO.parse(args.genome, "fasta"):
		
		seqid = seq.id
		sequence = str(seq.seq)
		
		if seqid in remove:
			pass
		
		elif seqid in trim:
			print('>'+seqid)
			for coords in trim[seqid][::-1]: #read in reverse order to start trimmming from the end. Allow to correclty trim with lower coordinates
				# print(coords)
				sequence = sequence[:int(coords[0])-1] + sequence[int(coords[1]):]
			while len(sequence) > 0:
				print(sequence[:70])
				sequence = sequence[70:]
		else:
			print('>'+seqid)
			while len(sequence) > 0:
				print(sequence[:70])
				sequence = sequence[70:]
		
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

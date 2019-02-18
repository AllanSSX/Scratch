#!/usr/bin/env python
# -*- coding: utf-8 -*-

#________________________________________________________________________________________________________________________________#

import argparse
from Bio import SeqIO
from Bio.SeqIO.FastaIO import FastaWriter

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-l',dest="list", type=argparse.FileType('r'),required=True,help='Fasta file with all single copy busco sequences')
	parser.add_argument('-s',dest="species",type=int,required=True,help='Minimal number of species per cluster')
	
	args = parser.parse_args()
	
	return args

def main(args):
	
	seqBUSCO = {}
	
	for line in args.list:
		BUSCO, status, gene_id, score, length = line.split()
		if not BUSCO in seqBUSCO:
			seqBUSCO[BUSCO] = {'seq':[gene_id], 'species':[gene_id.split("|")[0]]}
		else:
			seqBUSCO[BUSCO]['seq'].append(gene_id)
			seqBUSCO[BUSCO]['species'].append(gene_id.split("|")[0])
	
	for seqID, infos in sorted(seqBUSCO.items()):
		if (len(infos['species']) - len(set(infos['species']))) == 0 and len(infos['species']) >= args.species:
			outpout = open(seqID+'.lst','w')
			for seq in infos['seq']:
				outpout.write(seq+'\n')
			outpout.close()

		
if __name__ == '__main__':
	args = getArgs()
	main(args)
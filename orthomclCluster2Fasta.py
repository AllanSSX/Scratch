#!/usr/bin/env python

import argparse
from Bio import SeqIO


def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-g',dest="group",type=argparse.FileType('r'),required=True,help='Group file from OrthoMCL')
	parser.add_argument('-f',dest="fasta",type=str,required=True,help='goodProteins.fasta from OrthoMCL')
	parser.add_argument('-s',dest="species",type=int,required=True,help='Minimal number of species per cluster')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	proteins = SeqIO.to_dict(SeqIO.parse(args.fasta, "fasta"))

	groups = {}
	
	for line in args.group:
		cluster = line.split()[0][:-1]
		seqs = line.split()[1:]
		
		###
		
		groups[cluster] = {'seq':seqs, 'species':{}}
		for gene in seqs:
			specie, id = gene.split('|')
			if specie not in groups[cluster]['species']:
				groups[cluster]['species'][specie] = 1
			else:
				groups[cluster]['species'][specie] += 1
		
		###
		
		groups[cluster]['otho_sp'] = len(groups[cluster]['species'])
		groups[cluster]['otho_ge'] = len(groups[cluster]['seq'])
	
	for cluster, infos in sorted(groups.items()):
		if infos['otho_sp'] == infos['otho_ge'] == args.species:
		#if infos['otho_sp'] == args.species:
			out = open(cluster+'.fasta', 'w')
			for gene in groups[cluster]['seq']:
				out.write('>'+gene+'\n')
				sequence = str(proteins[gene].seq)
				while len(sequence) > 0:
					out.write(sequence[:70]+'\n')
					sequence = sequence[70:]
			out.close()

if __name__ == '__main__':
	args = getArgs()
	main(args)

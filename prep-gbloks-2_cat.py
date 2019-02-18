#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=argparse.FileType('r'),required=True,help='')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	# rename = {'masurca.roeselum.scaff.fasta':'DROE',
	# 		  'masurca.muelleri.scaff.fasta':'DMUE',
	# 		  'Nosema_antheraeae_YY.fasta':'NANT',
	# 		  'Nosema_apis_BRL_01.fasta':'NAPI',
	# 		  'Nosema_bombycis_CQ1.fasta':'NBOM',
	# 		  'Nosema_ceranae_PA08_1199.fna':'NCEP',
	# 		  'Nosema_granulosis.fasta':'NGRA',
	# 		  'Nosema_sp_YNPr.fasta':'NYNP'}
	
	for line in args.fasta:
		if line.startswith('>'):
			#eog, specie, contig, coordinates = line.split(':')
			specie, gene_id = line.split('|')
			print(specie.split('.')[0])
			
			# if specie in rename:
			# 	print('>'+rename[specie])
			# else:
			# 	print('>'+specie.split('.')[0])
			
			
			# print('>'+code2specie[line.split('|')[0][1:]])
			# print('>'+line.split('|')[0][1:])
		else:
			print(line[:-1])

if __name__ == '__main__':
	args = getArgs()
	main(args)

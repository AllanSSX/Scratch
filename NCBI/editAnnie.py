#!/usr/bin/env python

import argparse
import re

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-a',dest="annie",type=argparse.FileType('r'),required=True,help='Annie sprot file')
	parser.add_argument('-n',dest="names",type=argparse.FileType('r'),required=True,help='BAD_GENES_NAMES')
	parser.add_argument('-d',dest="description",type=argparse.FileType('r'),required=True,help='BAD_PRODUCT_DESCRIPTION')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	BAD_GENES_NAMES = {}
	for line in args.names:
		if not line.startswith('DiscRep'):
			FeaType, name, loc, gene_id = line.split()
			BAD_GENES_NAMES[gene_id] = None
	
	
	BAD_PRODUCT_DESCRIPTION = {}
	for line in args.description:
		if not line.startswith('DiscRep'):
			FeaType, descri, loc, gene_id = line.split('\t')
			BAD_PRODUCT_DESCRIPTION[gene_id[:-1]] = None
	
	for line in args.annie:
		gene_id, feature, description = line.split('\t')
		description = description[:-1]
		
		if feature == 'name':
			#TEST_BAD_GENE_NAME == remove 'name' line
			if not re.match("|".join(['ECU[0-9][0-9]', 'SP[A-Z][A-Z][0-9][0-9]', '^B11B22', '^IIV6', '[0-9][0-9][0-9][0-9]', 'HI_[0-9][0-9][0-9][0-9]', 'K02A2']), description):
				if not gene_id in BAD_GENES_NAMES:
					print(line[:-1])
					
		if feature == 'product':
			#SUSPECT_PRODUCT_NAMES == remove the last element + create a 'note' description with the full line
			if gene_id.split('.')[0] in BAD_PRODUCT_DESCRIPTION:
				
				if re.match('Uncharacterized', description):
					pass
				else:
					print(gene_id+'\tproduct\t'+' '.join(description.split()[:-1]))
					print(gene_id+'\tnote\t'+description)
			
			elif re.match('Uncharacterized', description):
				pass
			
			else:
				print(line[:-1])
		
		if feature == 'Dbxref':
			print(line[:-1])
		
		
		
		
		
		
		
		
		
		
		
		
		
if __name__ == '__main__':
	args = getArgs()
	main(args)

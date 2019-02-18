#!/usr/bin/env python

import argparse
from BCBio import GFF
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-g',dest="gff",type=str,required=True,help='gff3 file')
	parser.add_argument('-l',dest="list",type=argparse.FileType('r'),required=True,help='List ID')
	parser.add_argument('-o',dest="out",type=str,required=True,help='output')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	genes = {}
	
	for line in args.list:
		genes[line.split()[0]] = None
	
	out = open(args.out, "w")
	handle = open(args.gff)
	for rec in GFF.parse(handle):
		for gene in rec.features:
			if gene.id in genes:
				#print(gene)
				tmp = SeqRecord(rec.seq, rec.id)
				tmp.features = [gene]
				GFF.write([tmp], out)
		
	handle.close()
	out.close()
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

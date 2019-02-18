#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-p',dest="plot",type=argparse.FileType('r'),required=True,help='Plot file from Blobtools - mergeTaxifyMap2Cov.py')
	# parser.add_argument('-c',dest="cluster",type=argparse.FileType('r'),required=True,help='cluster info from PhylOligo')
	parser.add_argument('-b',dest="busco",type=argparse.FileType('r'),required=True,help='BUSCO list of contigs ID')
	# parser.add_argument('-n',dest="bins",type=argparse.FileType('r'),required=True,help='Clusters from MaxBin')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	# clusters = {}
	# 
	# for line in args.cluster:
	# 	contig_id, cluster_id = line.split()
	# 	clusters[contig_id] = cluster_id
	# 	
	# bins = {}
	# 
	# for line in args.bins:
	# 	contig_id, bin_id = line.split()
	# 	bins[contig_id] = bin_id
	
	busco = {}
	
	for line in args.busco:
		busco[line.split()[0]] = None
	
	
	print 'contig_id\tlength\tgc\tcoverage\ttax\tBUSCO'
	for line in args.plot:
		if not line.startswith("contig_id"):
			contig_id, length, gc, coverage, taxonomy = line.split()
			
			busco_id = 'no'
			if contig_id in busco:
				busco_id = 'yes'			
			
			print contig_id+'\t'+length+'\t'+gc+'\t'+coverage+'\t'+taxonomy+'\t'+busco_id
	
	# print 'contig_id\tlength\tgc\tcoverage\ttax\tclst\tbin\tBUSCO'
	# for line in args.plot:
	# 	if not line.startswith("contig_id"):
	# 		contig_id, length, gc, coverage, taxonomy = line.split()
	# 		
	# 		busco_id = 'no'
	# 		if contig_id in busco:
	# 			busco_id = 'yes'
	# 			
	# 		cluster = 'removed'	
	# 		if contig_id in clusters:
	# 			cluster = clusters[contig_id]
	# 		
	# 		bin = 'removed'	
	# 		if contig_id in bins:
	# 			bin = bins[contig_id]			
	# 		
	# 		print contig_id+'\t'+length+'\t'+gc+'\t'+coverage+'\t'+taxonomy+'\t'+cluster+'\t'+bin+'\t'+busco_id


if __name__ == '__main__':
	args = getArgs()
	main(args)

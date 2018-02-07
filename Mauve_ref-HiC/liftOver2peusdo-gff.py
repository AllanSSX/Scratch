#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-l',dest="liftover",type=argparse.FileType('r'),required=True,help='LiftOver file')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	# print("##gff-version 3")
	for line in args.liftover:
		if line.startswith("chain"):
			chain, id, sctg_id, sctg_lgth, sctg_strand, sctg_strart, sctg_end, chr_id, chr_lgth, chr_strand, chr_start, chr_end, chunk = line.split()
			
			if chr_strand=="-":
				chr_start_corr = int(chr_lgth) - int(chr_end)
				chr_end_corr = int(chr_lgth) - int(chr_start)
				
				chr_end = chr_end_corr
				chr_start = chr_start_corr
			
			if chr_start == '0':
				chr_start = 1
			
			print chr_id+"\tORCAE\tmisc_RNA\t"+str(chr_start)+"\t"+str(chr_end)+"\t.\t+\t.\tID="+sctg_id+";Name="+sctg_id

if __name__ == '__main__':
	args = getArgs()
	main(args)

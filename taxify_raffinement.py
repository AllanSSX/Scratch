#!/usr/bin/env python

import argparse
import re

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-k',dest="kingdom",type=argparse.FileType('r'),required=True,help='Taxify kingdom file')
	parser.add_argument('-p',dest="phylum",type=argparse.FileType('r'),required=True,help='Taxify phylum file')
	parser.add_argument('-s',dest="specie",type=argparse.FileType('r'),required=True,help='Taxify specie file')
	parser.add_argument('-c',dest="coverage",type=str,required=True,help='Coverage file from Blobtools')
	parser.add_argument('-b',dest="busco",type=argparse.FileType('r'),required=True,help='BUSCO scaffolds list')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	specie = {}
	kingdom = {}
	coverage = {}
	BUSCO = {}
	
	for line in args.busco:
		BUSCO[line.split()[0]] = None
	
	for line in open(args.coverage):
		if not line.startswith('#'):
			seq, reads, cov = line.split()
			coverage[seq] = [reads, cov]
	
	for line in args.kingdom:
		if not line.startswith('#'):
			# seq, reads, cov, size, gc, taxo = line.split()
			seq, size, gc, taxo = line.split()
			if re.split('=|;', taxo)[3].split(':')[0] == 'Fungi':
				kingdom[seq] = None
	
	for line in args.specie:
		if not line.startswith('#'):
			# seq, reads, cov, size, gc, taxo = line.split()
			seq, size, gc, taxo = line.split()
			if (re.split('=|;', taxo)[3].split(':')[0]).startswith('Papilio'):
				specie[seq] = None
	
	for line in args.phylum:
		if not line.startswith('#'):
			# seq, reads, cov, size, gc, taxo = line.split()
			seq, size, gc, taxo = line.split()
			if re.split('=|;', taxo)[3].split(':')[0] == 'Microsporidia':
				print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tL1')
			# 	print(line[:-1]+'\tL1')
			elif seq in specie:
				print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tL2')
			# 	print(line[:-1]+'\tL2')
			elif seq in kingdom:
				print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tL3')
			# 	print(line[:-1]+'\tL3')
			elif seq in BUSCO:
				print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tL4')
			# 	print(line[:-1]+'\tL4')
			elif re.split('=', taxo)[2].split(':')[0] == 'no-hit':
				print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tno-hit')
			else:
				print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tothers')
				# if re.search("Microsporidia", taxo):
				# 	print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tL5')
				# elif not re.search("Arthropoda", taxo):
				# 	print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tothers')
				# else:
				# 	print(seq+'\t'+'\t'.join(coverage[seq])+'\t'+size+'\t'+gc+'\t'+taxo+'\tArthropoda')
			
	
if __name__ == '__main__':
	args = getArgs()
	main(args)

#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=argparse.FileType('r'),required=True,help='')
	parser.add_argument('-l',dest="link",type=argparse.FileType('r'),required=True,help='Link between orthomcl codename and specie name')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	code2specie = {}
	for line in args.link:
		code, fasta = line.split()
		specie = fasta.split('.')[0]
		
		code2specie[code] = specie
	
	
	for line in args.fasta:
		if line.startswith('>'):
			print('>'+code2specie[line.split('|')[0][1:]])
			#print('>'+line.split('|')[0][1:])
		else:
			print(line[:-1])

if __name__ == '__main__':
	args = getArgs()
	main(args)

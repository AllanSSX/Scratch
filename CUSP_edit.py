#!/usr/bin/env python3

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="input",type=argparse.FileType('r'),required=True,help='')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	AA_code = {'A':'Ala',
			   'R':'Arg',
			   'D':'Asp',
			   'N':'Asn',
			   'C':'Cys',
			   'E':'Glu',
			   'Q':'Gln',
			   'G':'Gly',
			   'H':'His',
			   'I':'Ile',
			   'L':'Leu',
			   'K':'Lys',
			   'M':'Met',
			   'F':'Phe',
			   'P':'Pro',
			   'S':'Ser',
			   'T':'Thr',
			   'W':'Trp',
			   'Y':'Tyr',
			   'V':'Val',
			   '*':'STOP'}
	
	for line in args.input:
		Specie,Codon,AA,Fraction,Frequency,Number = line.split()
		if AA in AA_code:
			print(Specie+'\t'+Codon+'\t'+AA_code[AA]+'\t'+Fraction+'\t'+Frequency+'\t'+Number)
		else:
			print(line[:-1])

if __name__ == '__main__':
	args = getArgs()
	main(args)

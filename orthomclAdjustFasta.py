#!/usr/bin/env python

import argparse
import subprocess

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="input",type=argparse.FileType('r'),required=True,help='code\tfasta')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	for line in args.input:
		code,fasta = line.split()
		
		cmd = "/usr/local/genome2/orthomcl/bin/orthomclAdjustFasta {code} {fasta} 1".format(code=code, fasta=fasta)
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

if __name__ == '__main__':
	args = getArgs()
	main(args)

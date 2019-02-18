#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse



def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-i',dest="input", type=str,required=True,help='mosdepth.global.dist.txt')
	
	args = parser.parse_args()
	
	return args

def main(args):


	pairs = [map(float, x.split()[1:]) for x in open(args.input) if x.startswith("total")]

	total = 0
	lastp = 0
	for dp, p in pairs:
		    total += dp * (p - lastp)
		    lastp = p
	print(total)

	
if __name__ == '__main__':
	args = getArgs()
	main(args)

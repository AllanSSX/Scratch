#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="fasta",type=argparse.FileType('r'),required=True,help='')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	gff3 = open('output.gff3', 'w')
	gff3.write('##gff-version 3\n')
	for line in args.fasta:
		if line.startswith('>'):
			elem = line.split()
			
			chr = elem[2].split('=')[1].split(':')[0]
			id = elem[0][1:]
			# start = elem[2].split('=')[1].split(':')[1].split('-')[0]
			# end = elem[2].split('=')[1].split(':')[1].split('-')[1]
			start = elem[2].split('=')[1].split(':')[1]
			end = elem[2].split('=')[1].split(':')[2]
			strand = elem[2].split('=')[1].split(':')[3]
			source = 'silkPathDB'
			score = '.'
			phase = '.'
			gff3.write(chr+'\t'+source+'\t'+'gene'+'\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+id+';Name='+id+'\n')
			gff3.write(chr+'\t'+source+'\t'+'mRNA'+'\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+id+'.1;Parent='+id+';Name='+id+'.1\n')
			gff3.write(chr+'\t'+source+'\texon\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t.\tID='+id+'.1.1'+';Parent='+id+'.1\n')
			gff3.write(chr+'\t'+source+'\tCDS\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t'+'0'+'\tID=CDS:'+id+'.1.1'+';Parent='+id+'.1;Name='+id+'.1\n')

if __name__ == '__main__':
	args = getArgs()
	main(args)

#!/usr/bin/env python

import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-i',dest="info",type=argparse.FileType('r'),required=True,help='Info_frags')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	init = 0
	
	for line in args.info:
		if line.startswith(">"):
			# when starting over a new chromosome
			if init != 0:
				print chr_id+"\tORCAE\tmisc_RNA\t"+str(start)+"\t"+str(end)+"\t.\t+\t.\tID="+sctg_id+";Name="+sctg_id
			init = 1
			
			# init all values, first chromosome / new chromosome
			chr_id = line.split()[0][1:]
			start = 0
			end = 0
			
		elif line.startswith("init"):
			pass
		else:
			if start == 0:
				sctg_id = line.split()[0]
				start = 1
				end = end + (int(line.split()[4]) - int(line.split()[3]))
				# start = end
				
			else:
				if line.split()[0] == sctg_id :
					end = end + (int(line.split()[4]) - int(line.split()[3]))
					
				else:
					print chr_id+"\tORCAE\tmisc_RNA\t"+str(start)+"\t"+str(end)+"\t.\t+\t.\tID="+sctg_id+";Name="+sctg_id
					sctg_id = line.split()[0]
					start = end + 1
					end = end + (int(line.split()[4]) - int(line.split()[3]))
					
					
	print chr_id+"\tORCAE\tmisc_RNA\t"+str(start)+"\t"+str(end)+"\t.\t+\t.\tID="+sctg_id+";Name="+sctg_id


if __name__ == '__main__':
	args = getArgs()
	main(args)

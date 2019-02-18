#!/usr/bin/env python

import argparse
import sys
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-f',dest="flat",type=argparse.FileType('r'),required=True,help='flat annotation file (sorted + filtered)')
	# parser.add_argument('-p',dest="protein",type=str,required=True,help='protein file')
	# parser.add_argument('-l',dest="link",type=argparse.FileType('r'),required=True,help='Link btw prodigal gene and protein name')
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	# old = {}
	# ref = {}
	# gene = {}
	# cds = {}
	# cara = {}
	
	### split the flat file and create a new gene name
	print('##gff-version 3')
	for line in args.flat:
		chr, source, name, start, end, score, strand, phase = line.split()
		score = '.'
		chr = 'chrM'
		
		if source == 'mitos':
			print(chr+'\t'+source+'\t'+'gene'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+name+';Name='+name)
			print(chr+'\t'+source+'\t'+'mRNA'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+name+'.1;Parent='+name+';Name='+name)
			print(chr+'\t'+source+'\t'+'CDS'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID=CDS:'+name+'.1.1;Parent='+name+'.1;Name='+name)
			
		elif source == 'mitfi':
			if name.startswith('r'):
				print(chr+'\t'+source+'\t'+'gene'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+name+';Name='+name)
				print(chr+'\t'+source+'\t'+'rRNA'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID=rRNA:'+name+';Parent='+name+';Name='+name)
			else:
				name = name.split('(')[0]
				print(chr+'\t'+source+'\t'+'gene'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+name+';Name='+name)
				print(chr+'\t'+source+'\t'+'tRNA'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID=rRNA:'+name+';Parent='+name+';Name='+name)

			
		
		# if id not in old:
		# 	if chr not in ref:
		# 		ref[chr] = 10
		# 	name = chr + '_' + format(ref[chr], '06d')
		# 	ref[chr] += 10
		# 	old[id]=name
		# 	cara[name] = [chr, source, type, strand]
		# 	gene[name] = 1
		# 	cds[name] = {}
		# 	cds[name][gene[name]] = [start, end, score, strand, phase]
		# 	
		# 	# print(name, id)
		# 
		# else:
		# 	name = old[id]
		# 	gene[name] += 1
		# 	cds[name][gene[name]] = [start, end, score, strand, phase]
	
	### write the new gff3 file
	
	# gff3 = open('output.gff3', 'w')
	# gff3.write('##gff-version 3\n')
	# for gene in sorted(cds):
	# 	
	# 	### gene and mRNA part
	# 	chr = cara[gene][0]
	# 	source = cara[gene][1]
	# 	type = cara[gene][2]
	# 	start = cds[gene][1][0]
	# 	end = cds[gene][len(cds[gene])][1]
	# 	score = '.'
	# 	strand = cara[gene][3]
	# 	phase = '.'
	# 	id = gene
	# 	
	# 	gff3.write(chr+'\t'+source+'\t'+'gene'+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+id+';Name='+id+'\n')
	# 	gff3.write(chr+'\t'+source+'\t'+type+'\t'+start+'\t'+end+'\t'+score+'\t'+strand+'\t'+phase+'\tID='+id+'.1;Parent='+id+';Name='+id+'.1\n')
	# 	
	# 	### exons
	# 	structure = cds[gene]
	# 	for nb, struct in structure.items():
	# 		
	# 		start = struct[0]
	# 		end = struct[1]
	# 		phase = struct[4]
	# 		if phase == '.':
	# 			phase = 0
	# 		
	# 		# gff3.write(chr+'\t'+source+'\texon\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t.\tID='+gene+'.1;Parent='+gene+'.1\n')
	# 		gff3.write(chr+'\t'+source+'\texon\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t.\tID='+gene+'.1.'+str(nb)+';Parent='+gene+'.1\n')
	# 		if type == 'mRNA':
	# 			# gff3.write(chr+'\t'+source+'\tCDS\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t'+str(phase)+'\tID=CDS:'+gene+'.1;Parent='+gene+'.1;Name='+gene+'.1\n')
	# 			gff3.write(chr+'\t'+source+'\tCDS\t'+str(start)+'\t'+str(end)+'\t'+score+'\t'+strand+'\t'+str(phase)+'\tID=CDS:'+gene+'.1.'+str(nb)+';Parent='+gene+'.1;Name='+gene+'.1\n')
	# 
	# ### rename genes names in the protein file
	
	# prodigalLinkNames = {}
	# for line in args.link:
	# 	prot_id, gene_id = line.split()
	# 	prodigalLinkNames[prot_id] = gene_id
	# 
	# prot_fasta = open('protein.aa', 'w')
	# 
	# for seq in SeqIO.parse(args.protein, "fasta"):
	# 	
	# 	if not seq.id.startswith('NGR'):
	# 		try:
	# 			name = (old[seq.id[:-1]+'t'])
	# 			prot_fasta.write('>'+name+'\n')
	# 			sequence = str(seq.seq)
	# 			while len(sequence) > 0:
	# 				prot_fasta.write(sequence[:70]+'\n')
	# 				sequence = sequence[70:]
	# 		except:
	# 			pass
	# 	
	# 	elif seq.id.startswith('NGR'):
	# 		try:
	# 			gene_id = prodigalLinkNames[seq.id]
	# 			name = (old[gene_id])
	# 			prot_fasta.write('>'+name+'\n')
	# 			sequence = str(seq.seq)
	# 			while len(sequence) > 0:
	# 				prot_fasta.write(sequence[:70]+'\n')
	# 				sequence = sequence[70:]
	# 		except:
	# 			pass

if __name__ == '__main__':
	args = getArgs()
	main(args)

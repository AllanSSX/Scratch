#!/usr/bin/env python3

import argparse
from biocode import gff

def main():
	parser = argparse.ArgumentParser( description='Updates 9th-column key/value pairs in GFF file using a batch-update file')
	
	parser.add_argument('-i', '--input_file', type=str, required=True, help='A GFF3 file' )
	parser.add_argument('-o', '--output_file', type=str, required=True, help='Path to an output file to be created' )
	parser.add_argument('-t', '--type', type=str, required=False, help='Filter rows updated based on the 3rd (type) column' )
	
	args = parser.parse_args()
	
	outfh = open(args.output_file, 'wt')
	
	chr_lst = {}
	cdsexon_count = {}
	
	for line in open(args.input_file):
		cols = line.rstrip().split("\t")

		if len(cols) == 9:
			if args.type is None or args.type == cols[2]:
				
				
				#init. incrementeur for a new chromosome
				chr = cols[0]
				if not chr in chr_lst:
					chr_lst[chr] = None
					incr = 0
				#first feature must be "gene", init. first gene by 000010
				feature = cols[2]
				if feature == 'gene':
					incr += 10
				
				#split col 9
				atts = gff.column_9_dict(cols[8])
				if 'Name' in atts:
					atts.pop('Name')
				
				#change values
				if feature == 'gene':
					old_id = atts['ID']
					
					gene_id = chr + '_' + format(incr, '06d')
					atts['ID'] = gene_id
					
					new_id = gene_id
					
					print(old_id, new_id)
				
				# assume no isoforms
				elif feature in ['mRNA', 'tRNA']:
					
					mRNA_id = gene_id + '.1'
					
					atts['ID'] = mRNA_id
					atts['Parent'] = gene_id
					
					cdsexon_count[mRNA_id] = 1
					
				elif feature in ['CDS','exon']:
					cdsexon_id = mRNA_id + '.' + str(cdsexon_count[mRNA_id])
					
					atts['Parent'] = mRNA_id
					atts['ID'] = cdsexon_id
					
					if feature == 'CDS':
						atts['ID'] = 'CDS:' + cdsexon_id
					
					# allow exon / cds switch position 
					if not cdsexon_id in cdsexon_count:
						cdsexon_count[cdsexon_id] = None
					else:
						cdsexon_count[mRNA_id] += 1

				cols[8] = gff.build_column_9_from_dict(atts)

		outfh.write("\t".join(cols) + "\n")

if __name__ == '__main__':
    main()

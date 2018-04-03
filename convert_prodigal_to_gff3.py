#!/usr/bin/env python3

import argparse
import re
from biocode import gff, things

def main():
    parser = argparse.ArgumentParser( description='Convert GFF output from Prodigal into GFF3 format')

    ## output file to be written
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to a GFF file created by Prodigal' )
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to an output file to be created' )
    args = parser.parse_args()

    assemblies = dict()
    current_assembly = None
    
    gene = None
    mRNAs = dict()
    in_sequence = False
    current_sequence = None
    current_gene_comment_lines = list()

    ## Used for tracking the exon count for each gene (for ID purposes)
    exon_count_by_mRNA = dict()
    
    fout = open(args.output, mode='wt', encoding='utf-8')
    fout.write("##gff-version 3\n")

    for line in open(args.input):
        if line.startswith("#"):
            pass
        
        else:
            ##
            
            gene = None
            mRNAs = dict()
            in_sequence = False
            current_sequence = None
            current_gene_comment_lines = list()
            
            ##
                        
            cols = line.split("\t")

            if len(cols) != 9:
                continue

            mol_id = cols[0]
            feat_type = cols[2]
            feat_id = gff.column_9_value(cols[8], 'ID')
            
            ## initialize this assembly if we haven't seen it yet
            if mol_id not in assemblies:
                assemblies[mol_id] = things.Assembly(id=mol_id)
            
            current_assembly = assemblies[mol_id]
            
            if feat_type == "CDS":
                # gene
                gene = things.Gene(id=feat_id)
                gene.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6] )
                
                # mRNA
                mRNA = things.mRNA(id=feat_id+'.t1', parent=gene)
                mRNA.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6] )
                gene.add_mRNA(mRNA)
                mRNAs[mRNA.id] = mRNA
                if feat_id in exon_count_by_mRNA:
                    raise Exception( "ERROR: two different mRNAs found with same ID: {0}".format(feat_id) )
                else:
                    exon_count_by_mRNA[feat_id+'.t1'] = 0
                
                # CDS / exons
                parent_id = gff.column_9_value(cols[8], 'ID')+'.t1'
                
                ## sanity check that we've seen this parent
                if parent_id not in mRNAs:
                    raise Exception("ERROR: Found CDS column with parent ({0}) mRNA not yet in the file".format(parent_id))
                
                CDS = things.CDS(id=parent_id+'.cds', parent=mRNAs[parent_id])
                CDS.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6], phase=int(cols[7]) )
                mRNA.add_CDS(CDS)
                
                # exons weren't explicitly defined in the input file, so we need to derive new IDs for them
                exon_count_by_mRNA[parent_id] += 1
                exon_id = "{0}.exon{1}".format(parent_id, exon_count_by_mRNA[parent_id])
                
                exon = things.Exon(id=exon_id, parent=mRNAs[parent_id])
                exon.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6] )
                mRNA.add_exon(exon)
            
            ##
            
            gene.print_as(fh=fout, source='Prodigal_v2.6.3', format='gff3')

if __name__ == '__main__':
    main()

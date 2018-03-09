#!/usr/bin/env python
# -*- coding: utf-8 -*-


#________________________________________________________________________________________________________________________________#

import argparse
from Bio import SeqIO

#________________________________________________________________________________________________________________________________#


def getArgs():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-f',dest="flat",type=argparse.FileType('r'),help='Flat annotation file (sorted by coordinates and chr)')
    parser.add_argument('-p',dest="protein",type=str,required=True,help='protein file')
    parser.add_argument('-l',dest="link",type=argparse.FileType('r'),required=True,help='Link btw prodigal gene and protein name')
    
    arg = parser.parse_args()

    return arg

def main(arg):
    
    chrS = {}
    
    ### split the flat annotation file and store genes structure per chr
    
    for line in args.flat:
        chr, source, type, start, end, score, strand, phase, id = line.split()
        if type == 'mRNA':
            if chr not in chrS:
                chrS[chr] = {}
            
            if id not in chrS[chr]:
                chrS[chr][id] = [start, end]
            
            else:
                chrS[chr][id][1] = end
        
    ### extract protein length for each transcript
    
    prodigalLinkNames = {}
    for line in args.link:
        prot_id, gene_id = line.split()
        prodigalLinkNames[prot_id] = gene_id
        
    seqLen = {}
    for seq in SeqIO.parse(args.protein, "fasta"):
        ### genemark
        if seq.id.endswith('g'):
            id = seq.id[:-1]+'t'
        
        elif seq.id.startswith('NGR'):
            id = prodigalLinkNames[seq.id]
        
        seqLen[id] = len(seq.seq)
    
    ### loop over each chr to look at overlaping genes
    
    overlap = []
    
    for chr, geneS_ref in sorted(chrS.items()):
        for gene_ref in geneS_ref:
            for gene_tested in chrS[chr]:
                # test genes in the same chr
                start_ref = int(chrS[chr][gene_ref][0])
                end_ref = int(chrS[chr][gene_ref][1])
                
                start_tested = int(chrS[chr][gene_tested][0])
                end_tested = int(chrS[chr][gene_tested][1])
    
                if gene_ref != gene_tested and gene_ref not in overlap:
                    if start_ref >= start_tested and start_ref <= end_tested:
                        # print(gene_tested+'('+str(seqLen[gene_tested])+')'+' overlap '+gene_ref+'('+str(seqLen[gene_ref])+')')
                        overlap.append(gene_tested)
                        if seqLen[gene_tested] <= seqLen[gene_ref]:
                            print(gene_tested)
                        else:
                            print(gene_ref)
                            
                    elif end_ref >= start_tested and end_ref <= end_tested:
                        # print(gene_tested+'('+str(seqLen[gene_tested])+')'+' overlap '+gene_ref+'('+str(seqLen[gene_ref])+')')
                        if seqLen[gene_tested] <= seqLen[gene_ref]:
                            print(gene_tested)
                        else:
                            print(gene_ref)
                        
                        overlap.append(gene_tested)

# def main(arg):
# 
#     dicoRef = splitGFF(arg.ref)
#     findOverlap(dicoRef)
# 
# def splitGFF(gff):
# 
#     dico={}
#     for line in gff:
#         if not line.startswith('#'):
#             elem=line.split()
#             if elem[2] == 'mRNA':
#                 chr = elem[0]
#                 gene_id=str(elem[8]).split(';')[1].split('=')[1]
#                 if chr not in dico:
#                     dico[chr] = {}
#                     dico[chr][gene_id]=(elem[3], elem[4])
#                 else:
#                     dico[chr][gene_id]=(elem[3], elem[4])
#     return dico
# 
# def findOverlap(dicoRef):
# 
#     overlap = []
#     
#     for chr, genes_ref in sorted(dicoRef.items()):
#         for gene_ref in genes_ref:
#             for gene_tested in dicoRef[chr]:
#                 # test genes in the same chr
#                 start_ref = int(dicoRef[chr][gene_ref][0])
#                 end_ref = int(dicoRef[chr][gene_ref][1])
#                 
#                 start_tested = int(dicoRef[chr][gene_tested][0])
#                 end_tested = int(dicoRef[chr][gene_tested][1])
# 
#                 if gene_ref != gene_tested and gene_ref not in overlap:
#                     if start_ref >= start_tested and start_ref <= end_tested:
#                         print(gene_tested+' overlap '+gene_ref)
#                         overlap.append(gene_tested)
#                     elif end_ref >= start_tested and end_ref <= end_tested:
#                         print(gene_tested+' overlap '+gene_ref)
#                         overlap.append(gene_tested)


if __name__ == '__main__':
    args = getArgs()
    main(args)
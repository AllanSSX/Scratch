#!/usr/bin/env python

#title           :GC4GFF.py
#description     :
#author          :Alexandre Cormier acormier@sb-roscoff.fr
#date            :2014 02 17
#version         :1.0
#notes           :


#________________________________________________________________________________________________________________________________#

import argparse
import subprocess
import os
import sys

#________________________________________________________________________________________________________________________________#

def getArgs():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-f',dest="fasta",type=str,required=True,help="Fasta file")
    parser.add_argument('-g',dest="gff",type=str,required=True,help="gff3 annotation file")
    
    arg = parser.parse_args()
    
    return arg

def main(arg):
    
    dicoexon={}
    # dicointron={}
    dicomRNA={}
    
    bedNuke_cmd="nucBed -fi {fasta} -bed {gff}".format(fasta=arg.fasta, gff=arg.gff)
    process = subprocess.Popen(bedNuke_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    
    for line in process.stdout.readlines():
        line = line.decode()
        elem=line.split()
        
        if elem[2] == 'mRNA':
            mRNA=elem[8].split(';')[0].split('=')[1]
            GC=elem[-8]
            dicomRNA[mRNA]=GC
            
        elif elem[2] == 'exon':
            exon=elem[8].split(';')[1].split('=')[1]
            A=int(elem[-7]); C=int(elem[-6]); G=int(elem[-5]); T=int(elem[-4])
            
            if exon not in dicoexon:
                dicoexon[exon] = [A, C, G, T]
            else:
                dicoexon[exon][0] = dicoexon[exon][0] + A
                dicoexon[exon][1] = dicoexon[exon][1] + C
                dicoexon[exon][2] = dicoexon[exon][2] + G
                dicoexon[exon][3] = dicoexon[exon][3] + T
                      
        # elif elem[2] == 'intron':
        #     gene_id=elem[8].split('=')[1]
        #     A=elem[11]; C=elem[12]; G=elem[13]; T=elem[14]
        #     
        #     diconame='dico'+str(elem[2])
        #     
        #     if not eval(diconame).has_key(gene_id):
        #         eval(diconame)[gene_id]=[A, C, G, T]
        #     
        #     else:
        #         eval(diconame)[gene_id][0]=int(eval(diconame)[gene_id][0])+int(A)
        #         eval(diconame)[gene_id][1]=int(eval(diconame)[gene_id][0])+int(C)
        #         eval(diconame)[gene_id][2]=int(eval(diconame)[gene_id][0])+int(G)
        #         eval(diconame)[gene_id][3]=int(eval(diconame)[gene_id][0])+int(T)
        
    outprefix=os.path.splitext(os.path.basename(arg.fasta))[0]
    
    exonWrite=open(outprefix+'_exon-GC.txt', 'w')
    # intronWrite=open(outprefix+'_intron-GC.txt', 'w')
    geneWrite=open(outprefix+'_mRNA-GC.txt', 'w')
    
    for key in sorted(dicomRNA):
        geneWrite.write(key+'\t'+dicomRNA[key]+'\n')
        exonWrite.write(key+'\t'+str((dicoexon[key][1]+dicoexon[key][2])/(dicoexon[key][0]+dicoexon[key][1]+dicoexon[key][2]+dicoexon[key][3]))+'\t'+'\t'.join(map(str, dicoexon[key]))+'\n')
    #     if dicointron.has_key(key):
    #         intronWrite.write(key+'\t'+str((float(dicointron[key][1])+float(dicointron[key][2]))/(float(dicointron[key][0])+float(dicointron[key][1])+float(dicointron[key][2])+float(dicointron[key][3]))*100)+'\n')
    # 
    exonWrite.close()
    # intronWrite.close()
    geneWrite.close()
   
if __name__ == '__main__':
    args = getArgs()
    main(args)

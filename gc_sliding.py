#!/usr/bin/env python
# -*- coding: utf-8 -*-

#================================================================#

import argparse
from Bio import SeqIO

#================================================================#

def getArgs():
    parser = argparse.ArgumentParser(description="",version="1.0.0")
    parser.add_argument('-f',dest="fasta",type=str,required=True,help='fasta file')
    parser.add_argument('-w',dest="win",type=int,required=True,help='window size')
    parser.add_argument('-p',dest="pos",type=argparse.FileType('r'),required=True,help='Position to compute')
    
    args = parser.parse_args()

    return args

def get_positions(pos_file):
    
    posDict = {}
    
    for line in pos_file:
        chr, pos = line.split()
        if not posDict.has_key(chr):
            posDict[chr] = [int(pos)]
        else:
            posDict[chr].append(int(pos))

    return posDict

def get_fasta(fasta_file, window, pos):
    
    fasta_seq = SeqIO.parse(open(fasta_file),'fasta')
    for fasta in fasta_seq:
        chr, sequence = fasta.id, str(fasta.seq)
        if pos.has_key(chr):
            for position in pos[chr]:
                get_GC(chr, sequence, window, position)
    
def get_GC(name, fasta, window, pos):
    
    start = pos - window
    stop = pos + window
    
    subseq = fasta[start:stop]
    print "%s\t%d\t%s" % (name, pos, calculate_gc(subseq))
    
def calculate_gc(dna):
    c_count = dna.count('C')
    g_count = dna.count('G')
    a_count = dna.count('A')
    t_count = dna.count('T')
    n_count = dna.count('N')
    
    gc_content = (g_count + c_count) / float(g_count + c_count + a_count + t_count + n_count)
    return gc_content
    
def main(args):
    
    pos = get_positions(args.pos)
    get_fasta(args.fasta, args.win, pos)
    
if __name__ == '__main__':
    args = getArgs()
    main(args)

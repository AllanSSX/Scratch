#!/bin/bash
#SBATCH --job-name=SOAPdenovo
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=10G
#SBATCH --partition=large
#SBATCH --error=%x.sh.e%A
#SBATCH --output=%x.sh.o%A

module load bioinf
module load SOAPdenovo2/r241

cfg=soap.cfg

SOAPdenovo-127mer pregraph -p 32 -s ${cfg} -K 57 -R -o SOAPdenovo
SOAPdenovo-127mer contig -p 32 -g SOAPdenovo -R
SOAPdenovo-127mer map -p 32 -s ${cfg} -g SOAPdenovo
SOAPdenovo-127mer scaff -g SOAPdenovo -F -N 1200000000

scaffolds2contigs.py -i SOAPdenovo.fasta -g 0 -s 500 > SOAPdenovo.sctg.fasta

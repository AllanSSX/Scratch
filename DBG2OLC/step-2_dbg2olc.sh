#!/bin/bash
#SBATCH --job-name=dbg2olc
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=100G
#SBATCH --partition=large
#SBATCH --error=%x.sh.e%A
#SBATCH --output=%x.sh.o%A

module load bioinf
module load DBG2OLC/current

unitigs=SOAPdenovo.sctg.fasta
pacbio=/home/acormier/scratch/a.vulgare/0-data/pacbio.a.vulgare.fasta

DBG2OLC LD 0 k 17 AdaptiveTh 0.01 KmerCovTh 2 MinOverlap 300 RemoveChimera 0 Contigs ${unitigs} f ${pacbio}

#10x/20x PacBio data: KmerCovTh 2-5, MinOverlap 10-30, AdaptiveTh 0.001~0.01.

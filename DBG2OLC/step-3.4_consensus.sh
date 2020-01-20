#!/bin/bash
#SBATCH --job-name=consensus
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --partition=large
#SBATCH --error=%x.sh.e%A
#SBATCH --output=%x.sh.o%A

cat 3-subReads/*.consensus.fasta > consensus.fasta


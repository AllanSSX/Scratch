#!/bin/bash
#SBATCH --job-name=consensus
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=100G
#SBATCH --partition=large
#SBATCH --error=%x.sh.e%A
#SBATCH --output=%x.sh.o%A

# 0 - prep
mkdir 1-backbone 2-splitReads

# 1 - decoupage du fichier fasta en plusieurs sous fichiers avec x sequences dedans
splitMutliFasta.py -i ${backbone} -o 1-backbone/ -n 100

# 2 - decoupage du fichier info en accord avec le decoupage du fichier fasta
splitDBG2OLC_consensusID.py -i ${DBG2OLC_Consensus_info} -o 2-splitReads/ -n 100

# 3 - suppression de l'extension .fasta (sinon plantage)
rename.pl 's/.fasta//' 2-splitReads/*.fasta

# 4 - concatenation des reads pacbio avec les contigs de l'assemblage Illumina
cat ${pbReads} ${contigs} > sctg_pb.fasta


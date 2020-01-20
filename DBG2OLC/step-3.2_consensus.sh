#!/bin/bash
#SBATCH --job-name=consensus
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=100G
#SBATCH --partition=large
#SBATCH --error=%x.sh.e%A.%a
#SBATCH --output=%x.sh.o%A.%a
#SBATCH --array=1-156
## valeur max de l'array a adapter en fonction du nombre de fichier fasta dans 1-backbone/

module load bioinf
module load DBG2OLC/current


backbone=`ls 1-backbone/*.fasta | awk "NR==$SLURM_ARRAY_TASK_ID"`
ID=`basename $backbone .backbone_raw.fasta`
DBG2OLC_Consensus_info=2-splitReads/${ID}.DBG2OLC_Consensus_info.txt
reads=reads.fasta

# 0 - prep
mkdir 3-subReads

# 1 - les reads sont separes en fonction du backbone qu'ils ont permit de construire
split_reads_by_backbone.py -b ${backbone} -o 3-subReads/reads${ID}/ -r ${reads} -c ${DBG2OLC_Consensus_info}


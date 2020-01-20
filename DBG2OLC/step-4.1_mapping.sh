#!/bin/bash
#SBATCH --job-name=bowtie2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=10G
#SBATCH --partition=large
#SBATCH --error=%x.sh.e%A
#SBATCH --output=%x.sh.o%A

module load bioinf
module load samtools/1.9
module load bowtie2/2.3.4.3

WXf1543_R1=/home/acormier/scratch/a.vulgare/0-data/PE_WXf1543femaleA.R1.gz
WXf1543_R2=/home/acormier/scratch/a.vulgare/0-data/PE_WXf1543femaleA.R2.gz

fasta=consensus.fasta

bowtie2-build --threads ${SLURM_CPUS_PER_TASK} ${fasta} ${fasta%.*}

bowtie2 --non-deterministic -p $((${SLURM_CPUS_PER_TASK}-4)) -q --fr --no-unal -I 100 -X 600 --sensitive -x ${fasta%.*} -1 ${WXf1543_R1} -2 ${WXf1543_R2} | samtools sort -o ${fasta%.*}.bam -@ 4 -m 8G -O bam -T tmp -

samtools index ${fasta%.*}.bam

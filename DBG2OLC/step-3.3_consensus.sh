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

## penser a mettre sans dans un script propre...

module load bioinf
module load anaconda3/conda3
source activate blasr

iterations=2

folder=`ls 3-subReads/ | awk "NR==$SLURM_ARRAY_TASK_ID"`
folder=3-subReads/${folder}

for fasta in $(find ${folder} -name "*.reads.fasta")
do
        chunk=`basename $fasta .reads.fasta`

        cmd=""
        for iter in `seq 1 ${iterations}`
        do
                cmd+="blasr --nproc 1 ${folder}/${chunk}.reads.fasta ${folder}/${chunk}.fasta --bestn 1 -m 5 --minMatch 19 --out ${folder}/${chunk}.mapped.m5; "
                cmd+="Sparc m ${folder}/${chunk}.mapped.m5 b ${folder}/${chunk}.fasta k 1 c 2 g 1 HQ_Prefix Contig boost 5 t 0.2 o ${folder}/${chunk}; "
                if [ ${iter} -lt ${iterations} ]
                then
                cmd+="mv ${folder}/${chunk}.consensus.fasta ${folder}/${chunk}.fasta;"
                fi
        done

        echo $cmd
        eval $cmd
        #to save space
        cmd="rm ${folder}/${chunk}.mapped.m5"
        echo $cmd
        eval $cmd
        cmd="rm ${folder}/${chunk}.reads.fasta"
        echo $cmd
        eval $cmd
done

#!/bin/bash

if [ $# -lt 2 ]
then
        echo "Usage: splitBam.sh <bam file> <chr list>"
        exit 1
fi

BAM=$1
CHRLIST=$2

for chr in $(cat $CHRLIST)
do
    echo $chr
    samtools view -H $BAM | grep '@HD' > $chr.sam
    samtools view -H $BAM | grep -P "SN:$chr\t" >> $chr.sam
    samtools view -H $BAM | grep '@PG' >> $chr.sam
    samtools view $BAM $chr >> $chr.sam
    samtools view -Sb $chr.sam > $chr.bam
    #rm -f $chr.bam
    echo "Done"
done

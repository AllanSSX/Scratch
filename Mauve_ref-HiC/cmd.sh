#!/bin/bash

#ref
split_fasta.py -f Ectsi_genome_V3.fasta
liftOver2peusdo-gff.py -l genetic_map.chain.sctg > chr_sctg.gff3
for i in $(cut -f1 chr_sctg.gff3 | sort | uniq); do grep ${i} chr_sctg.gff3 > ${i}.gff3; done

for fasta in *.fasta; do fasta2gbk.py -f ${fasta} -g ${fasta%.*}.gff3 -o ${fasta%.*}; done

#HiC
split_fasta.py -f Ectsi_genome_HiC.fasta
rename.pl 's/-assembly|/_/' *.fasta
sed -i 's/-assembly|/_/' 3C_*.fasta

info_frags2gff3.py -i info_frags.txt | sed 's/-assembly|/_/' > chr_HiC.gff3
for i in $(cut -f1 chr_sctg.gff3 | sort | uniq); do grep ${i} chr_HiC.gff3 > ${i}.gff3; done

for fasta in *.fasta; do fasta2gbk.py -f ${fasta} -g ${fasta%.*}.gff3 -o ${fasta%.*}; done

#Mauve
while read -r hic sctg
do
    progressiveMauve --output=output/${sctg}.mauve --output-guide-tree=output/${sctg}.guide_tree --backbone-output=output/${sctg}.backbone ${sctg}.gb ${hic}.gb
done < chr.lst

#!/bin/bash

# Requirements: BWA, sam2fasta.py, abifpy

# Error reporting
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <directory_of_ab1_files> <reference_gene_coding_sequence> <gene>" >&2
  echo "gene is pfcrt, pfmdr1, dhfr or dhps"
  exit 1
fi
if ! [ -e "$1" ]; then
  echo "$1 not found" >&2
  echo "Usage: $0 <directory_of_ab1_files> <reference_gene_coding_sequence> <gene>" >&2
  echo "gene is pfcrt, pfmdr1, dhfr or dhps"
  exit 1
fi
if [[ ! -d "$1" || -L "$1" ]]; then
  #If argument is not a directory or is a symbolic link
  echo "$1 not a directory" >&2
  echo "Usage: $0 <directory_of_ab1_files> <reference_gene_coding_sequence> <gene>" >&2
  echo "gene is pfcrt, pfmdr1, dhfr or dhps"
  exit 1
fi

# 1. Call bases from .ab1 files and output concatenated fastq file of all samples
./get_fastq_ab1.sh $1 $3

# 2. Align sample sequences to reference coding sequence of same gene
bwa index $2    # index reference sequence
bwa bwasw $2 $1$3*$(date +%d_%m_%y)*fastq > $1$3_$(date +%d_%m_%y).sam


# 3. Convert SAM alignment to fasta using sam2fasta.py
#    written by Chang Park available here: http://sourceforge.net/projects/sam2fasta/files/
#    Usage: sam2fasta.py [ref.fasta] [in.sam] [out.fasta]
./sam2fasta.py $2 $1$3_$(date +%d_%m_%y).sam $1$3_$(date +%d_%m_%y).fasta

# 4. Parse FASTA alignment to output SNPs at specific codons and their corresponding amino acid changes
./main.py -i $1$3_$(date +%d_%m_%y).fasta -g $3
#!/bin/bash

# Requirements: BWA, sam2fasta.py, abifpy, fastq-mcf

# Error reporting
if ! [ "$#" -ge 3 ]; then
  echo "Usage: $0 <directory_of_ab1_files> <reference_gene_coding_sequence> <gene> <quality_cutoff>" >&2
  echo "gene is pfcrt, pfmdr1, dhfr or dhps"
  echo "<quality_cutoff> is between 0 and 1. quality_cutoff is optional"
  exit 1
fi
if ! [ -e "$1" ]; then
  echo "$1 not found" >&2
  echo "Usage: $0 <directory_of_ab1_files> <reference_gene_coding_sequence> <gene> <quality_cutoff>" >&2
  echo "gene is pfcrt, pfmdr1, dhfr or dhps"
  echo "<quality_cutoff> is between 0 and 1. quality_cutoff is optional"
  exit 1
fi
if [[ ! -d "$1" || -L "$1" ]]; then
  #If argument is not a directory or is a symbolic link
  echo "$1 not a directory" >&2
  echo "Usage: $0 <directory_of_ab1_files> <reference_gene_coding_sequence> <gene> <quality_cutoff>" >&2
  echo "gene is pfcrt, pfmdr1, dhfr or dhps"
  echo "<quality_cutoff> is between 0 and 1. It is optional."
  exit 1
fi

# 1. Call bases from .ab1 files and output concatenated fastq file of all samples
./get_fastq_ab1.sh $1 $3

# 2. Filter bases using PHRED quality score
if test ! -e $1$3_$(date +%d_%m_%y); then
    echo "Error: missing fastq file. Ensure that directory contains .ab1 files."
    exit 1
else
    if [ "$#" -ge 4 ] && [ "$4" -gt 0 ] && [ "$4" -lt 93 ]; then
        ./ea-utils.1.1.2-806/fastq-mcf n/a $1$3*_$(date +%d_%m_%y).fastq -o $1$3_q$4_$(date +%d_%m_%y).fastq -q $4
    else
        ./ea-utils.1.1.2-806/fastq-mcf n/a $1$3*_$(date +%d_%m_%y).fastq -o $1$3_q10_$(date +%d_%m_%y).fastq -q 10
    fi
fi

# 2. Align sample sequences to reference coding sequence of same gene
if test ! -e $1$3_q*$(date +%d_%m_%y).fastq; then
    echo "Error: Missing filtered fastq file."
    exit 1
else
    ./bwa-0.7.12/bwa index $2    # index reference sequence
    ./bwa-0.7.12/bwa bwasw $2 $1$3_q*$(date +%d_%m_%y).fastq > $1$3_$(date +%d_%m_%y).sam
fi

# 3. Filter reads by mapping quality
if test ! -e $1$3_$(date +%d_%m_%y).sam; then
    echo "Error: missing SAM alignment file."
    exit 1
else
    ./samtools-1.2/samtools view -Sq 2 $1$3_$(date +%d_%m_%y).sam > $1$3_flt_$(date +%d_%m_%y).sam
fi

# 4. Convert SAM alignment to fasta using sam2fasta.py
#    written by Chang Park available here: http://sourceforge.net/projects/sam2fasta/files/
#    Usage: sam2fasta.py [ref.fasta] [in.sam] [out.fasta]
if test ! -e $1$3_flt_$(date +%d_%m_%y).sam; then
    echo "Error: missing filtered SAM alignment file."
    exit 1
else
    ./sam2fasta.py $2 $1$3_flt_$(date +%d_%m_%y).sam $1$3_$(date +%d_%m_%y).fasta
fi

# 5. Parse FASTA alignment to output SNPs at specific codons and their corresponding amino acid changes
if test ! -e $1$3_$(date +%d_%m_%y).fasta; then
    echo "Error: missing FASTA alignment file."
    exit 1
else
    ./adr_codons.py -i $1$3_$(date +%d_%m_%y).fasta -g $3
fi

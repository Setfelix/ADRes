#!/bin/bash
# Bash script to automate recursive task of converting ab1 files to fastq, and concatenate them into single fastq
# file

# Error reporting
if ! [ "$#" -ge 2 ]; then
  echo "Usage: $0 <directory_of_ab1_files> <gene> " >&2
  echo "gene is pfcrt, pfmdr1, dhfr or dhps"
  exit 1
fi

#  enable filename patterns which match no files to expand to a null string, rather than themselves
shopt -s nullglob;

total_ab1=0 #count the number of ab1 files
ab1_dir=$1 # directory where ab1 files are located
gene=$2

#remove any fastq files in ab1_dir if they exist
fastq_files=($ab1_dir*.fastq)
if [[ "${#fastq_files[@]}" -gt 0 ]] ; then
  cd $ab1_dir
  rm *.fastq
  cd -
fi

for file in ${ab1_dir}*.ab1
  do
    #print current file
    echo "processing..." ${file##*/}
    python ab1_to_fastq.py $file
    total_ab1=$((total_ab1+1))
  done;


echo "Done converting $total_ab1 ab1 files to fastq.";

cat *.fastq > $ab1_dir/${gene}_$(date +%d_%m_%y).fastq;

#remove individual fastq files after concatenating them
rm *.fastq

shopt -u nullglob; #disable nullglob option for shell


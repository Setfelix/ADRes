#!/bin/bash
# Bash script to automate recursive task of converting single ab1 files to fastq and concatenate them into single fastq
# file

shopt -s nullglob; #[set shell option behavior] enable filename patterns which match no files to expand to a null string, rather than themselves.

if [[ -d "$1" && ! -L "$1" ]]; then

  total_ab1 = 0; #count the number of ab1 files
  ab1_dir = $1 # directory where ab1 files are located
  gene = $2

  for file in ${ab1_dir}/*.ab1
  do
    echo "processing..." $file
    python ab1_to_fastq.py $file
    total_ab1 = $((total_ab1+1)) #increase the total number of ab1 files by 1
  done;
  echo "Done converting $total_ab1 ab1 files to fastq.";
  cat *.fastq > ${gene}_${total_ab1}_$(date +%d_%m_%y).fastq;


else

  echo "Directory does not exist and/or no gene provided."
  echo "Usage: get_fastq_ab1.sh <directory of ab1 files> <gene name>"

fi

shopt -u nullglob; #disable nullglob option for shell
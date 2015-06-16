#!/bin/bash
# Bash script to automate recursive task of converting ab1 files to fastq, and concatenate them into single fastq
# file

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

# check whether quality_cutoff has been given
if [ "$#" -eq 3 ]; then
  p_cutoff=$3
  for file in ${ab1_dir}*.ab1
  do
    echo "processing..." $file
    python ab1_to_fastq.py $file $p_cutoff
    #increase the total number of ab1 files by 1
    total_ab1=$((total_ab1+1))
  done;
else
  for file in ${ab1_dir}*.ab1
  do
    echo "processing..." $file
    python ab1_to_fastq.py $file
    #increase the total number of ab1 files by 1
    total_ab1=$((total_ab1+1))
  done;
fi

echo "Done converting $total_ab1 ab1 files to fastq.";

cat *.fastq > $ab1_dir/${gene}_$((total_ab1))_$(date +%d_%m_%y).fastq;

#remove individual fastq files after concatenating them
rm *.fastq

shopt -u nullglob; #disable nullglob option for shell


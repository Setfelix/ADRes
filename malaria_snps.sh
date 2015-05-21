#!/bin/bash

# Error reporting
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <directory of ab1 files> <gene name>" >&2
  echo "gene name is pfcrt, pfmdr1, dhfr or dhps"
  exit 1
fi
if ! [ -e "$1" ]; then
  echo "$1 not found" >&2
  echo "Usage: $0 <directory of ab1 files> <gene name>" >&2
  echo "gene name is pfcrt, pfmdr1, dhfr or dhps"
  exit 1
fi
if [[ ! -d "$1" || -L "$1" ]]; then
  #If argument is not a directory or is a symbolic link
  echo "$1 not a directory" >&2
  echo "Usage: $0 <directory of ab1 files> <gene name>" >&2
  echo "gene name is pfcrt, pfmdr1, dhfr or dhps"
  exit 1
fi

# 1. Call bases from .ab1 files and output fastq file
./get_fastq_ab1.sh $1 $2

#Convert SAM alignment to fasta using sam2fasta.py
#written by Chang Park available here: http://sourceforge.net/projects/sam2fasta/files/
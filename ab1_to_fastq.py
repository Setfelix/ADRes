#! /usr/bin/python
__author__ = 'sefel'

from abifpy import Trace  # python module for reading ab1 files (https://github.com/bow/abifpy)
import sys  # for file input, output operations

q_score_cutoff = 20  # cutoff for filtering reads based on PHRED quality score
f_seq = ''  # f - filtered
f_qual = ''
f_qual_val = []

if len(sys.argv) <= 1:
    print "No inputfile provided."
    print "Usage: python ab1_to_fastq.py <inputfile.ab1>"
    sys.exit()
else:
    inputfile = sys.argv[1]
    # trims based on PHRED quality score using modified Richard Mott's algorithm
    my_seq = Trace(inputfile, trimming=True)
    for i in range(0, len(my_seq.qual_val)):
        #filter sequence based on q_score_cutoff
        if my_seq.qual_val[i] >= q_score_cutoff:
            f_seq += my_seq.seq[i]
            f_qual_val.append(my_seq.qual_val[i])
            f_qual += my_seq.qual[i]
    #set filtered values as default for my_seq
    my_seq.seq = f_seq
    my_seq.qual = f_qual
    my_seq.qual_val = f_qual_val
    # replace ambiguous code with Ns
    my_seq.seq = my_seq.seq_remove_ambig(my_seq.seq)
    my_seq.export(my_seq.name + ".fastq", 'fastq')

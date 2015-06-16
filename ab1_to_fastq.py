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
    if len(sys.argv) == 3:
        q_prob_cutoff = sys.argv[2]
        # begin trimming using modified Richard Mott's algorithm with custom error probability cutoff
        my_seq = Trace(inputfile)
        my_seq.seq = my_seq.trim(my_seq.seq, q_prob_cutoff)
        my_seq.qual = my_seq.trim(my_seq.qual, q_prob_cutoff)
        my_seq.qual_val = my_seq.trim(my_seq.qual_val, q_prob_cutoff)
    else:
        # trim sequence using modified Richard Mott's algorithm with default error probability cutoff (0.05)
        my_seq = Trace(inputfile, trimming=True)
    # replace ambiguous code with Ns
    my_seq.seq = my_seq.seq_remove_ambig(my_seq.seq)
    my_seq.export(my_seq.name + ".fastq", 'fastq')

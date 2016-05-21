__author__ = 'sefel'
# ! /usr/bin/python

# This script takes a DNA fasta alignment, of dhfr(cds) and sample sequences (of same gene), as input and outputs a csv file of sample_id, codon(s), and amino acid

# import required modules
import re  # regex requirements
import csv  # to write csv files
import operator  # helps to sort items in list

import adr_codons


ofile = ''
sample_list = []  # list of sample and codon information as class object


def write2csv(sl, of):
    """write effect of codons, i.e amino acid change, for each sample in tab-delimited file like this:
    Sample, Codon_position(one or more), Amino acid"""

    # sort sample list by sample name
    sl.sort(key=operator.attrgetter('name'))
    # write samples to csv file
    with open(of, 'wb') as out:
        sampleWriter = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        sampleWriter.writerow(["Sample", "codon_51", "codon_51_aa", "codon_59_aa", "codon_59_aa", "codon_108",
                               "codon_108_aa", "codon_164", "codon_164_aa"])
        for c in sl:
            sampleWriter.writerow([c.name, c.codon_51, c.codon_51_aa, c.codon_59, c.codon_59_aa, c.codon_108,
                                   c.codon_108_aa, c.codon_164, c.codon_164_aa])


# make a class (codon) to store codons at different positions for each sample

class codon(object):
    # create a class of codons and their corresponding amino acids
    def __init__(self, name, codon_51, codon_51_aa, codon_59, codon_59_aa, codon_108, codon_108_aa, codon_164,
                 codon_164_aa):
        self.name = name
        self.codon_51 = codon_51
        self.codon_51_aa = codon_51_aa
        self.codon_59 = codon_59
        self.codon_59_aa = codon_59_aa
        self.codon_108 = codon_108
        self.codon_108_aa = codon_108_aa
        self.codon_164 = codon_164
        self.codon_164_aa = codon_164_aa


def sample_class(seq_name, cd51, cd51aa, cd59, cd59aa, cd108, cd108aa, cd164, cd164aa):
    sample = codon(seq_name, cd51, cd51aa, cd59, cd59aa, cd108, cd108aa, cd164, cd164aa)
    sample_list.append(sample)
    write2csv(sample_list, ofile)  # write codons, amino acids to CSV file
    return sample_list


def read_inputfile(inputfile, outputfile, *args):
    # read input file and generate list of samples with codon information

    # read fasta alignment file
    with open(inputfile, 'r') as infile:
        inlines = infile.readlines()

    # regular expressions
    ref_seq_id_pattern = r'^>PfCRT.+$'
    seq_id_pattern = r'^>'
    seq_pattern = r'^[AGTCN*\.]+$'

    ref_seq_id_rx = re.compile(ref_seq_id_pattern)
    seq_id_rx = re.compile(seq_id_pattern)
    seq_rx = re.compile(seq_pattern)

    ref_codon_info = []
    ref_seq_id_line = 0
    ref_seq = ""


    # GET CODONS FOR SPECIFIC POSITIONS ON REFERENCE SEQUENCE

    #************************************************************************************************************
    #
    #Using oop to get codons for each sample
    #Adapted from: http://www.daniweb.com/software-development/python/code/216631/a-list-of-class-objects-python
    #************************************************************************************************************

    #get seq_id for sequence
    for i in xrange(0, len(inlines), 2):
        #sample_list=[]
        seq_id = ""
        #get header line
        if seq_id_rx.search(inlines[i]):
            seq_id += inlines[i].rstrip('\n')
            seq_id = seq_id.lstrip('>')
            #print seq_id
        #get codons for each seq
        #print "now ready for codons of this sequence..."
        codon_number = 0
        codon_51 = ""
        codon_59 = ""
        codon_108 = ""
        codon_164 = ""
        i_seq = ""
        if seq_rx.search(inlines[i + 1]):
            i_seq += str(inlines[i + 1].rstrip('\n'))
            #print str(len(i_seq))
            for s in xrange(0, len(i_seq) - 3, 3):
                codon = i_seq[s:s + 3]
                codon_number += 1
                if codon_number == 51:
                    codon_51 += codon
                elif codon_number == 59:
                    codon_59 += codon
                elif codon_number == 108:
                    codon_108 += codon
                elif codon_number == 164:
                    codon_164 += codon

        #pass sample and codon information to sample_class function to create codon object etc.
        sample_class(seq_id, codon_51, adr_codons.amino_acid(codon_51), codon_59, adr_codons.amino_acid(codon_59),
                     codon_108,
                     adr_codons.amino_acid(codon_108), codon_164, adr_codons.amino_acid(codon_164))

    return outputfile










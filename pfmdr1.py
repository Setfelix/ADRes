__author__ = 'sefel'
# ! /usr/bin/python

# This script takes a DNA fasta alignment, of pfmdr1(cds) and sample sequences (of same gene), as input and outputs a csv file of sample_id, codon(s), and amino acid

# import required modules
import re  # regex requirements
import csv  # to write csv files
import operator  # helps to sort items in list

import main


ofile = ''
sample_list = []  # list of sample and codon information as class object


def write2csv(sl, of):
    """write effect of codons, i.e amino acid change, for each sample in tab-delimited file like this:
    Sample, Codon_position(one or more), Amino acid"""

    # sort sample list by sample name
    sl.sort(key=operator.attrgetter('name'))
    # write samples to csv file
    with open(of, 'wb') as out:
        sampleWriter = csv.writer(out, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
        sampleWriter.writerow(["Sample", "Codon_86", "Codon_86_aa", "Codon_184", "Codon_184_aa", "Codon_1034",
                               "Codon_1034_aa", "Codon_1042", "Codon_1042_aa", "Codon_1246", "Codon_1246_aa"])
        for c in sl:
            sampleWriter.writerow([c.name, c.codon_86, c.codon_86_aa, c.codon_184, c.codon_184_aa, c.codon_1034,
                                   c.codon_1034_aa, c.codon_1042, c.codon_1042_aa, c.codon_1246, c.codon_1246_aa])


# make a class (codon) to store codons at different positions for each sample

class codon(object):
    # create a class of codons and their corresponding amino acids
    def __init__(self, name, codon_86, codon_86_aa, codon_184, codon_184_aa, codon_1034, codon_1034_aa, codon_1042,
                 codon_1042_aa, codon_1246, codon_1246_aa):
        self.name = name
        self.codon_86 = codon_86
        self.codon_86_aa = codon_86_aa
        self.codon_184 = codon_184
        self.codon_184_aa = codon_184_aa
        self.codon_1034 = codon_1034
        self.codon_1034_aa = codon_1034_aa
        self.codon_1042 = codon_1042
        self.codon_1042_aa = codon_1042_aa
        self.codon_1246 = codon_1246
        self.codon_1246_aa = codon_1246_aa


def sample_class(seq_name, cd86, cd86aa, cd184, cd184aa, cd1034, cd1034aa, cd1042, cd1042aa, cd1246, cd1246aa):
    sample = codon(seq_name, cd86, cd86aa, cd184, cd184aa, cd1034, cd1034aa, cd1042, cd1042aa, cd1246, cd1246aa)
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


    #GET CODONS FOR SPECIFIC POSITIONS ON REFERENCE SEQUENCE

    #************************************************************************************************************
    #
    #Using oop to get codons for each sample
    #Adapted from: http://www.daniweb.com/software-development/python/code/216631/a-list-of-class-objects-python
    #************************************************************************************************************

    #get seq_id for sequence
    for i in xrange(0, len(inlines) - 2, 2):
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
        codon_86 = ""
        codon_184 = ""
        codon_1034 = ""
        codon_1042 = ""
        codon_1246 = ""
        i_seq = ""
        if seq_rx.search(inlines[i + 1]):
            i_seq += str(inlines[i + 1].rstrip('\n'))
            #print str(len(i_seq))
            for s in xrange(0, len(i_seq) - 3, 3):
                codon = i_seq[s:s + 3]
                codon_number += 1
                if codon_number == 86:
                    codon_86 += codon
                elif codon_number == 184:
                    codon_184 += codon
                elif codon_number == 1034:
                    codon_1034 += codon
                elif codon_number == 1042:
                    codon_1042 += codon
                elif codon_number == 1246:
                    codon_1246 += codon

        #pass sample and codon information to sample_class function to create codon object etc.
        sample_class(seq_id, codon_86, main.amino_acid(codon_86), codon_184, main.amino_acid(codon_184), codon_1034,
                     main.amino_acid(codon_1034), codon_1042, main.amino_acid(codon_1042), codon_1246,
                     main.amino_acid(codon_1246))

    return outputfile










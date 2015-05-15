__author__ = 'sefel'
# ! /usr/bin/python

# This script takes a DNA fasta alignment, of dhps(cds) and sample sequences (of same gene), as input and outputs a csv file of sample_id, codon(s), and amino acid

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
        sampleWriter.writerow(["Sample", "codon_436", "codon_436_aa", "codon_437", "codon_437_aa", "codon_540",
                               "codon_540_aa", "codon_581", "codon_581_aa", "codon_613", "codon_613_aa"])
        for c in sl:
            sampleWriter.writerow([c.name, c.codon_436, c.codon_436_aa, c.codon_437, c.codon_437_aa, c.codon_540,
                                   c.codon_540_aa, c.codon_581, c.codon_581_aa, c.codon_613, c.codon_613_aa])


# make a class (codon) to store codons at different positions for each sample

class codon(object):
    # create a class of codons and their corresponding amino acids
    def __init__(self, name, codon_436, codon_436_aa, codon_437, codon_437_aa, codon_540, codon_540_aa, codon_581,
                 codon_581_aa, codon_613, codon_613_aa):
        self.name = name
        self.codon_436 = codon_436
        self.codon_436_aa = codon_436_aa
        self.codon_437 = codon_437
        self.codon_437_aa = codon_437_aa
        self.codon_540 = codon_540
        self.codon_540_aa = codon_540_aa
        self.codon_581 = codon_581
        self.codon_581_aa = codon_581_aa
        self.codon_613 = codon_613
        self.codon_613_aa = codon_613_aa


def sample_class(seq_name, cd436, cd436aa, cd437, cd437aa, cd540, cd540aa, cd581, cd581aa, cd613, cd613aa):
    sample = codon(seq_name, cd436, cd436aa, cd437, cd437aa, cd540, cd540aa, cd581, cd581aa, cd613, cd613aa)
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
        codon_436 = ""
        codon_437 = ""
        codon_540 = ""
        codon_581 = ""
        codon_613 = ""
        i_seq = ""
        if seq_rx.search(inlines[i + 1]):
            i_seq += str(inlines[i + 1].rstrip('\n'))
            #print str(len(i_seq))
            for s in xrange(0, len(i_seq) - 3, 3):
                codon = i_seq[s:s + 3]
                codon_number += 1
                if codon_number == 436:
                    codon_436 += codon
                elif codon_number == 437:
                    codon_437 += codon
                elif codon_number == 540:
                    codon_540 += codon
                elif codon_number == 581:
                    codon_581 += codon
                elif codon_number == 613:
                    codon_613 += codon

        #pass sample and codon information to sample_class function to create codon object etc.
        sample_class(seq_id, codon_436, main.amino_acid(codon_436), codon_437, main.amino_acid(codon_437), codon_540,
                     main.amino_acid(codon_540), codon_581, main.amino_acid(codon_581), codon_613,
                     main.amino_acid(codon_613))

    return outputfile










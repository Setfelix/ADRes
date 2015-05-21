#! /usr/bin/python
__author__ = 'sefel'

import getopt
import sys
import os  # standard imports
import re  # regular expressions
import time
# gene-specific imports
import pfcrt
import pfmdr1
import dhps
import dhfr


outputfile_location = sys.path[0]


def usage():
    print "\nThis script takes a DNA fasta alignment file as input and outputs a csv file of sample_id, codon(s), and amino acid."
    print "Contact: Setor Amuzu, felixsetor@yahoo.com"
    print "Usage: python main.py -i <inputfile.fas> -g <gene_name>"
    print "Example: python main.py -i bwasw_pfcrt_aln.fas -g pfcrt"
    print "Where inputfile is a fasta alignment of reference gene sequence and individual sample sequences of same gene."
    print "The following antimalarial drug resistance genes and codons are currently supported: "
    print "pfmdr1: 86, 184"
    print "pfcrt: 72,73,74,75,76"
    print "dhps: 436, 437, 540, 581, 613"
    print "dhfr: 51, 59, 108, 164\n"


def inputfile_chk(inputfile, gene):
    # check if inputfile is indeed a file
    if not os.path.isfile(inputfile):
        print "Input file not found"
        sys.exit()
    else:
        # global outputfile
        # check for .fas or .fasta extension
        regex = re.match(".*?\.fas$", inputfile)
        regex2 = re.match(".*?\.fasta$", inputfile)
        if regex:
            outputfile = inputfile[:-4] + "_" + time.strftime(
                '%d%m%Y') + ".csv"  # remove last four characters and append our output extension
            print "This is outputfile: %s" % (outputfile)
            pfcrt.ofile = outputfile
            pfcrt.read_inputfile(inputfile, outputfile)  # pass input file to read_inputfile to run lines
            pfcrt.ofile = outputfile
        elif regex2:
            outputfile = inputfile[:-6] + ".csv"
            print outputfile
            pfcrt.ofile = outputfile
            if gene == 'pfcrt':
                pfcrt.read_inputfile(inputfile, outputfile)
            elif gene == 'pfmdr1':
                # go to pfmdr1 parser
                pfmdr1.read_inputfile(inputfile, outputfile)
            elif gene == 'dhps':
                # go to dhps parser
                dhps.read_inputfile(inputfile, outputfile)
            elif gene == 'dhfr':
                # pass inputfile to dhfr parser
                dhfr.read_inputfile(inputfile, outputfile)
        else:
            print "File must be fasta format and needs \".fas\" or \".fasta\" extension.\n Recheck file and try again.\n"
            sys.exit()
    return outputfile


def amino_acid(codon):
    # translated codon
    # what does codon translate to?
    # create dictionary of codon(key): amino acid pairs(value) using DNA genetic code
    codon_dict = {"TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
                  "ATT": "I", "ATC": "I",
                  "ATA": "I", "ATG": "M", "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V", "TCT": "S", "TCC": "S",
                  "TCA": "S", "TCG": "S", "CCT": "P",
                  "CCC": "P", "CCA": "P", "CCG": "P", "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCT": "A",
                  "GCC": "A", "GCA": "A", "GCG": "A", "TAT": "Y",
                  "TAC": "Y", "TAA": "STOP", "TAG": "STOP", "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q", "AAT": "N",
                  "AAC": "N", "AAA": "K", "AAG": "K",
                  "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "TGT": "C", "TGC": "C", "TGA": "STOP", "TGG": "W",
                  "CGT": "R", "CGC": "R", "CGA": "R",
                  "CGG": "R", "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R", "GGT": "G", "GGC": "G", "GGA": "G",
                  "GGG": "G"}
    for key in codon_dict:
        if codon == key:
            aa = codon_dict[key]
            break
        elif codon != key:
            aa = "-"
            next
    return aa


def initiate(argv):
    inputfile = ''
    gene_name = ''
    try:
        opts, args = getopt.getopt(argv, "hi:g:", ["input", "gene"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
            print 'Input file is: %s' % (str.split(inputfile, '/')[-1])
        elif opt in ("-g", "--gene="):
            gene_name = str(arg)
            gene_name = gene_name.lower()
            if gene_name == 'pfcrt':
                print 'SNPs in codons 72, 73, 74, 75, 76 of pfcrt gene will be reported.'
            elif gene_name == 'pfmdr1':
                print 'SNPs in codons 86, 184 of pfmdr1 will be reported.'
            elif gene_name == 'dhps':
                print 'SNPs in codons 436, 437, 540, 581, 613 will be reported.'
            elif gene_name == 'dhfr':
                print 'SNPs in codons 51, 59, 108, 164 will be reported.'
                # print 'Codon positions of interest are: ' + ','.join(str(p) for p in codon_positions)
            inputfile_chk(inputfile, gene_name)  # QC inputfile

    return inputfile, gene_name

# begin executing script
if __name__ == "__main__":
    if len(sys.argv) <= 1:  # check if at least one argument is passed to script
        usage()
        sys.exit()

    else:
        initiate(sys.argv[1:])
        sys.exit(0)

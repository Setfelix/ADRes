Detect SNPs in codons of antimalarial drug resistance genes
===========================================================
This repository is a collection of scripts used to identify SNPs in specific codons of Plasmodium falciparum genes that
are implicated with antimalarial drug resistance. Currently, the following genes are supported pfcrt, pfmdr1, dhps, dhfr.

If no command line arguments are given, the following information is displayed:

This script takes a DNA fasta alignment file as input and outputs a csv file of sample_id, codon(s), and amino acid.
Contact: Setor Amuzu, felixsetor@yahoo.com
Usage: python pfcrt_codons2csv.py inputfile.fas

Where inputfile is a fasta alignment of reference pfcrt gene sequence and individual sample sequences of same gene.

Example:

-------------------------------------------------------------------------------------------------------------
Inputfile (obtained by converting bwa bwasw SAM alignment file to fasta format)
-------------------------------------------------------------------------------------------------------------

>Ref_pfcrt_gene
AAAGAGATTAAGGATAATATTTTTATTTATATTTTAAGTATTATTTATTTAAGTGTATGTGTAATGAATAAAATTTTTGCT
>Sample_1
AAAGAGA*TAAGGATAATATTTTTATTTATATTTTAAGTATTATTTATTTAAGTGTATGTGTAATTGAAACAATTTTTGCT
>Sample_2
AAAGAGA*TAAGG**AATATTTTTATTTATATTTTAAGTATTATTTATTTAAGTGTATGTGTAATG***AAAATTTTTGCT

-------------------------------------------------------------------------------------------------------------
Outputfile_pfcrt_codons_72_76.csv
-------------------------------------------------------------------------------------------------------------

"Sample"	"Codon_72"	"Codon_72_aa"	"Codon_73"	"Codon_73_aa"	"Codon_74"	"Codon_74_aa"	"Codon_75"	"Codon_75_aa"	"Codon_76"	"Codon_76_aa"
"Ref_pfcrt_gene"	"TGT"	"C"	"GTA"	"V"	"ATT"	"I"	"GAA"	"E"	"ACA"	"T"
"Sample_1"	"TGT"	"C"	"GTA"	"V"	"ATG"	"M/ START"	"***"	"-"	"AAA"	"K"
"Sample_2"	"TGT"	"C"	"GTA"	"V"	"ATG"	"M/ START"	"AAT"	"N"	"AAA"	"K"

-------------------------------------------------------------------------------------------------------------
Command line
-------------------------------------------------------------------------------------------------------------

python main.py inputfile.fas



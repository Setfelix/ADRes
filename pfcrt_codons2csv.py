#! /usr/bin/python

#This script takes a DNA fasta alignment file as input and outputs a csv file of sample_id, codon(s), and amino acid.

#import required modules
import getopt, sys #for handling options
import os, string # standard imports
import re #regex requirements
import csv #to write csv files
import operator #helps to sort items in list

sample_list=[] #list of sample and codon information as class object
 
def usage():
  print "This script takes a DNA fasta alignment file as input and outputs a csv file of sample_id, codon(s), and amino acid."
  print "Contact: Setor Amuzu, felixsetor@yahoo.com"
  print "Usage: python pfcrt_codons2csv.py inputfile.fas\n"
  print "Where inputfile is a fasta alignment of reference pfcrt gene sequence and individual sample sequences of same gene."
  
  
def inputfile_chk(inputfile):
  #check if inputfile is indeed a file
  if not(os.path.isfile(inputfile)):
    print "Input file not found"
    sys.exit()
  else:
    global outputfile
    #print str(inputfile)
    # check for .fas or .fasta extension
    regex=re.match(".*?\.fas$", inputfile)
    regex2=re.match(".*?\.fasta$", inputfile)
    if regex:
      outputfile = inputfile[:-4] + "_pfcrt_codons_72_76.csv" # remove last four characters and append our output extension
      read_inputfile(inputfile, outputfile) #pass input file to read_inputfile to run lines
    elif regex2:
      outputfile = inputfile[:-6] + "_pfcrt_codons_72_76.csv"
      read_inputfile(inputfile, outputfile) #pass input file to read_inputfile to run lines
    else:
      print "File must be fasta format and needs \".fas\" or \".fasta\" extension.\n Recheck file and try again.\n"
      sys.exit()
  return inputfile, outputfile
  
def write2csv():
  """write effect of codons, i.e amino acid change, for each sample in tab-delimited file like this:
  Sample, Codon_position(one or more), Amino acid"""
  
  #sort sample list by sample name
  sample_list.sort(key=operator.attrgetter('name')) 
  #write samples to csv file
  with open(outputfile, 'wb') as out:
    
    sampleWriter=csv.writer(out, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
    sampleWriter.writerow(["Sample","Codon_72","Codon_72_aa","Codon_73","Codon_73_aa","Codon_74","Codon_74_aa",
    "Codon_75","Codon_75_aa","Codon_76","Codon_76_aa"])
    for c in sample_list:
      sampleWriter.writerow([c.name,c.codon_72,c.codon_72_aa,c.codon_73,c.codon_73_aa,c.codon_74,c.codon_74_aa,
      c.codon_75,c.codon_75_aa,c.codon_76,c.codon_76_aa])
  print
  usage()
  print
  print "Output file name is %s. It is saved in %s directory." %(outputfile, sys.path[0])
  print
 
def amino_acid(codon):
  #translated codon
  #what does codon translate to?
  #create dictionary of codon(key): amino acid pairs(value) using DNA genetic code
  codon_dict={"TTT":"F", "TTC":"F", "TTA":"L", "TTG":"L", "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L", "ATT":"I", "ATC":"I",
  "ATA":"I", "ATG":"M/ START", "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V", "TCT":"S", "TCC":"S", "TCA":"S", "TCG":"S", "CCT":"P",
  "CCC":"P", "CCA":"P", "CCG":"P", "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T", "GCT":"A", "GCC":"A", "GCA":"A", "GCG":"A", "TAT":"Y",
  "TAC":"Y", "TAA":"STOP", "TAG":"STOP", "CAT":"H", "CAC":"H", "CAA":"Q", "CAG":"Q", "AAT":"N", "AAC":"N", "AAA":"K", "AAG":"K",
  "GAT":"D", "GAC":"D", "GAA":"E", "GAG":"E", "TGT":"C", "TGC":"C", "TGA":"STOP", "TGG":"W", "CGT":"R", "CGC":"R", "CGA":"R", 
  "CGG":"R", "AGT":"S", "AGC":"S", "AGA":"R", "AGG":"R", "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G"}
  for key in codon_dict:
    if codon==key:
      aa=codon_dict[key]
      break
    elif codon!=key:
      aa="-"
      next
  return aa
  
	  
#make a class (codon) to store codons at different positions for each sample

class codon(object):
  #create a class of codons and their corresponding amino acids
  def __init__(self,name,codon_72,codon_72_aa,codon_73,codon_73_aa,codon_74,codon_74_aa,codon_75,codon_75_aa,codon_76,codon_76_aa):
    self.name=name
    self.codon_72=codon_72
    self.codon_72_aa=codon_72_aa
    self.codon_73=codon_73
    self.codon_73_aa=codon_73_aa
    self.codon_74=codon_74
    self.codon_74_aa=codon_74_aa
    self.codon_75=codon_75
    self.codon_75_aa=codon_75_aa
    self.codon_76=codon_76
    self.codon_76_aa=codon_76_aa  

def sample_class(seq_name,cd72,cd72aa,cd73,cd73aa,cd74,cd74aa,cd75,cd75aa,cd76,cd76aa):
  sample=codon(seq_name,cd72,cd72aa,cd73,cd73aa,cd74,cd74aa,cd75,cd75aa,cd76,cd76aa)
  sample_list.append(sample)
    
  return sample_list

def read_inputfile(inputfile, outputfile):
  #read input file and generate list of samples with codon information
  
  #read fasta alignment file
  with open(inputfile, 'r') as infile:
    inlines=infile.readlines()
  
  #regular expressions
  ref_seq_id_pattern=r'^>PfCRT.+$'
  seq_id_pattern=r'^>'
  seq_pattern=r'^[AGTCN*\.]+$'
  
  ref_seq_id_rx=re.compile(ref_seq_id_pattern)
  seq_id_rx=re.compile(seq_id_pattern)
  seq_rx=re.compile(seq_pattern)
  
  ref_codon_info=[]
  ref_seq_id_line=0
  ref_seq=""
  

  #GET CODONS FOR SPECIFIC POSITIONS ON REFERENCE SEQUENCE

  #************************************************************************************************************
  #
  #Using oop to get codons for each sample
  #Adapted from: http://www.daniweb.com/software-development/python/code/216631/a-list-of-class-objects-python
  #************************************************************************************************************
  
  #get seq_id for sequence
  for i in xrange(0,len(inlines)-2,2):
    #sample_list=[]
    seq_id=""
    #get header line
    if seq_id_rx.search(inlines[i]):
      seq_id+=inlines[i].rstrip('\n')
      seq_id=seq_id.lstrip('>')
      #print seq_id
    #get codons for each seq
    #print "now ready for codons of this sequence..."
    codon_number=0
    codon_72=""
    codon_73=""
    codon_74=""
    codon_75=""
    codon_76=""
    i_seq=""
    if seq_rx.search(inlines[i+1]):
      i_seq+=str(inlines[i+1].rstrip('\n'))
      #print str(len(i_seq))      
      for s in xrange(0,len(i_seq)-3,3):
	codon=i_seq[s:s+3]
	codon_number+=1
	if codon_number==72:
	  codon_72+=codon
	elif codon_number==73:
	  codon_73+=codon
	elif codon_number==74:
	  codon_74+=codon
	elif codon_number==75:
	  codon_75+=codon
	elif codon_number==76:
	  codon_76+=codon
	  
    #pass sample and codon information to sample_class function to create codon object etc.
    sample_class(seq_id,codon_72,amino_acid(codon_72),codon_73,amino_acid(codon_73),codon_74,amino_acid(codon_74),codon_75,
    amino_acid(codon_75),codon_76,amino_acid(codon_76))
   
  return  


def main(arg):
  inputfile=arg[1]
  inputfile_chk(inputfile) #pass inputfile to inputfile_chk function
  #print "inputfile passed to inputfile_chk function"
  
  return
    
#begin executing script
if __name__ == "__main__":
    if len(sys.argv) <= 1: #check if at least one argument is passed to script
      usage()
      sys.exit()
      
    else:
      main(sys.argv)
      #print "inputfile passed to main function"
      write2csv() #write sample_list information to csv file
      sys.exit(0)



  

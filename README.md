ADRes: a pipeline to detect molecular markers of Antimalarial Drug Resistance
=============================================================================
`adres.sh` is a BASH-scripted pipeline that can be used to identify SNPs in specific codons of 
_Plasmodium falciparum_ genes that are associated with antimalarial drug resistance, from Sanger sequencing data. 
Currently, the following genes and codons are supported:

| Gene     | Codons                   |
|----------|:------------------------:|
| _pfmdr1_ | 86, 184, 1034, 1042,1246 |
| _pfcrt_  | 72, 73, 74, 75, 76       |
| _dhps_   | 436, 437, 540, 581, 613  |
| _dhfr_   | 51, 59, 108, 164         |

Using ABI Sanger sequencing trace files of whole gene (or regions spanning codons of interest) from several samples, 
this pipeline outputs a CSV-formatted file of sample name, codons and their corresponding amino acids.

This pipeline is a combination of existing tools (such as [BWA](http://bio-bwa.sourceforge.net/), [sam2fasta.py](http://sourceforge.net/projects/sam2fasta/files/), [abifpy](https://github.com/bow/abifpy), [SAMtools](http://www.htslib.org/)) and custom scripts, and is made up of the following steps:

1. Base calling and quality control, 
2. Alignment of filtered sequences to coding sequence of respective reference gene, 
3. SAM alignment filtering and conversion to FASTA format, 
4. Parse FASTA alignment to output codons and corresponding amino acid in CSV format.

-----------------------------------------------------------
Installation
-----------------------------------------------------------
1. Download the source [`.zip`](https://github.com/Setfelix/anti_malaria_snps/zipball/master) or [`.tar.gz`](https://github.com/Setfelix/anti_malaria_snps/tarball/master) file and extract
2. Optionally, add the ADRes directory to your `$PATH` (in `.bashrc`, for example, to make it persistent 

------------------------------------------------------------------------------------------------------------------------
Usage
------------------------------------------------------------------------------------------------------------------------

         bash adres.sh <directory_of_ab1_files> <reference_gene_coding_sequence> <gene> [quality_cutoff]
where: 
        
        <directory_of_ab1_files> is directory containing ab1 trace files of a single gene (pfcrt, pfmdr1, dhps, or dhfr)
        <reference_gene_coding_sequence> is path to reference coding sequence of respective gene
        <gene> is pfcrt, pfmdr1, dhps, or dhfr
        [quality_cutoff] is the Phred quality threshold for trimming bases. 
                        This argument is OPTIONAL. Default value is 10 (Q10).
                        Legal values range from 10 to 60.
        
-------------------------------------------------------------------------------------------------------------
Example command
-------------------------------------------------------------------------------------------------------------
        bash adres.sh ~/pfcrt_ab1_seq/ ~/anti_mdr_snps/pfcrt_pf3D7_cds.fasta pfcrt 

------------------------------------------------------------------------------------------------------------
Output
------------------------------------------------------------------------------------------------------------
The primary output file is named in this format: `gene_dd_mm_yy.csv` and is stored in the `<directory_of_ab1_files>`
The output for the example command above could look like this:

| Sample   | Codon_72 | Codon_72_aa | Codon_73 | Codon_73_aa | Codon_74 | Codon_74_aa | Codon_75 | Codon_75_aa | Codon_76 | Codon_76_aa |
|----------|:--------:|:-----------:|:--------:|:-----------:|:--------:|:-----------:|:--------:|:-----------:|:--------:|:-----------:|
| 89C_CRT  | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 90C_CRT  | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 92C_CRT  | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 93C_CRT  | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 94C_CRT  | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 97C_CRT  | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 99C_CRT  | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| PfCRT_ref| TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |

------------------------------------------------------------------------------------------------------------
Example data
------------------------------------------------------------------------------------------------------------

The archived file containing the source code for this pipeline also contains some `example_data`.
The `example_data` directory contains:

1. `example_ab1`             : This directory contains 50 ab1 trace files obtained from sequencing regions of _pfcrt_ 
                               spanning codons 72 - 76 from 50 _P. falciparum_ isolates.
                               This directory can be used as `<directory_of_ab1_files>`. 
                               It also contains 3 intermediate files (`pfcrt_30_06_15.fasta`, `pfcrt_30_06_15.sam`, 
                               `pfcrt_30_06_15.fastq`) and the main output file (`pfcrt_30_06_15.csv`).
                               Typically, `<directory_of_ab1_files>` will not contain any intermediate files or 
                               output file until you have ran the pipeline successfully.
                              
2. `pfcrt_pf3d7_cds.fasta`   : The reference coding sequence for _pfcrt_ [PlasmoDB: PF3D7_0709000]. 
                               This file can be used as `<reference_gene_coding_sequence>`. 
                               Reference was originally downloaded from [plasmodb.org](http://plasmodb.org/plasmo/).
   
                              

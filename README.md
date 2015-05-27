Detect SNPs in codons of antimalarial drug resistance genes
===========================================================
`malaria_snps.sh` is a BASH-scripted pipeline that can be used to identify SNPs in specific codons of 
_Plasmodium falciparum_ genes that are associated with antimalarial drug resistance. 
Currently, the following genes are supported _pfcrt, pfmdr1, dhps, dhfr_.

Using Sanger sequencing ab1 trace files of whole gene (or regions spanning codons of interest) from several samples, 
this pipeline outputs a CSV-formatted file of sample name, codons and their corresponding amino acid.

This pipeline is a combination of existing tools (such as BWA) and custom scripts and is made up of the following steps:

1. base calling and quality control, 
2. alignment of trimmed and filtered sequences to coding sequence of respective reference gene, 
3. conversion of alignment from SAM to FASTA format, 
4. Parse FASTA alignment to output codons and corresponding amino acid in CSV format.

-----------------------------------------------------------
Usage
-----------------------------------------------------------

         bash malaria_snps.sh <directory_of_ab1_files> <reference_gene_coding_sequence> <gene>
where: 
        
        <directory_of_ab1_files> is directory containing ab1 trace files of a single gene
        <reference_gene_coding_sequence> is path to reference coding sequence
        <gene> is pfcrt, pfmdr1, dhps, or dhfr
        
-------------------------------------------------------------------------------------------------------------
Example
-------------------------------------------------------------------------------------------------------------
 bash malaria_snps.sh ~/pfcrt_ab1_seq/ ~/anti_mdr_snps/pfcrt_pf3D7_cds.fasta pfcrt

-------------------------------------------------------------------------------------------------------------
Sample output
-------------------------------------------------------------------------------------------------------------

| Sample    | Codon_72 | Codon_72_aa | Codon_73 | Codon_73_aa | Codon_74 | Codon_74_aa | Codon_75 | Codon_75_aa | Codon_76 | Codon_76_aa |
|-----------|----------|-------------|----------|-------------|----------|-------------|----------|-------------|----------|-------------|
| 89C_CRT_F | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 90C_CRT_F | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 92C_CRT_F | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 93C_CRT_F | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 94C_CRT_F | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 97C_CRT_F | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| 99C_CRT_F | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |
| PfCRT_ref | TGT      | C           | GTA      | V           | ATG      | M           | AAT      | N           | AAA      | K           |


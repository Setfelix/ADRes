#read data
#data is from example_data in ADRes GitHub repo, which can be downloaded here: 
#https://github.com/Setfelix/anti_malaria_snps/tarball/master
adr_snps<-read.csv('pfcrt_30_06_15.csv', h=T, sep = '\t')
#create column for haplotype
adr_snps$haplotype<-with(adr_snps,paste(Codon_72_aa, Codon_73_aa, Codon_74_aa, Codon_75_aa, Codon_76_aa ,sep=''))
#frequency of haplotypes, excluding reference haplotype
table(adr_snps$haplotype[-length(adr_snps$haplotype)])
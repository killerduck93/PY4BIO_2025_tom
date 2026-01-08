# genbank files
from Bio import SeqIO
for seq_record in SeqIO.parse("sequence.gb", "genbank"):
    print(seq_record)
    #added to print just one record example
    break

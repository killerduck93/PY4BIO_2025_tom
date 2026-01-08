# genbank files
from Bio import SeqIO
for seq_record in SeqIO.parse("sequence.gb", "genbank"):
    print(seq_record.id)
    print(repr(seq_record.seq))
    print(len(seq_record))

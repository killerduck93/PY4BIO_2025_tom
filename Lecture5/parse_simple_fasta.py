# Parse a simple fasta file
from Bio import SeqIO
for seq_record in SeqIO.parse("multi_fasta_gb_header.fasta", "fasta"):
    print( seq_record.id )
    #print( repr(seq_record.seq) )
    print( seq_record.seq )
    print( len(seq_record) )
    break

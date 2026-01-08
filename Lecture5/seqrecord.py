from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

## create a simple SeqRecord object
simple_seq = Seq( "GATCAGGATTAGGCC" )
simple_seq_r = SeqRecord( simple_seq )
simple_seq_r.id = "AC12345"
simple_seq_r.description = "I am not a real sequence"

## print summary
print( simple_seq_r.id )
print( simple_seq_r.description )
print( str(simple_seq_r.seq) )
#print( simple_seq_r.seq.alphabet )

## translate the sequence
translated_seq = simple_seq_r.seq.translate()
print ( translated_seq )

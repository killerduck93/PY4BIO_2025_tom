from Bio.Seq import Seq
try:
    from Bio.Alphabet.IUPAC import ambiguous_dna
except ImportError:
    ambiguous_dna = None

if ambiguous_dna:
    dna_seq = Seq("ACRGT", ambiguous_dna)
else:
    dna_seq = Seq("ACRGT")
    
print( dna_seq )

# A Seq object in python acts like a normal python string.

for letter in dna_seq:
    print( letter )

print( 'Length: ', len(dna_seq) )
print( dna_seq[4:12] )
print( dna_seq[::-1] )
print(type(dna_seq))
print( str(dna_seq) )

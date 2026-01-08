from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

# The Seq objects no longer have a .alphabet attribute, 
# and do not do type checking on Seq operations like adding protein to DNA anymore. 
# Remove references to Alphabet where necessary:

# from Bio.Alphabet.IUPAC import unambiguous_dna, ambiguous_dna

# my_seq = Seq("AGTACACTGGTA", unambiguous_dna)
my_seq = Seq("AGTACACTGGTA")

print(my_seq)

# How many As, Cs, Ts, and Gs in this sequence?
print('# A: ', my_seq.count("A"))
print('# C: ', my_seq.count("C"))
print('# T: ', my_seq.count("T"))
print('# G: ', my_seq.count("G"))

# Calculate GC content
gc_content = gc_fraction(my_seq) * 100

# Transcription and translation
my_mRNA = my_seq.transcribe()
print( my_mRNA )
my_pept = my_seq.translate()
print( my_pept )

# Complement and reverse complement
print( 'sequence: ',str(my_seq) )
print( 'comp.: ',my_seq.complement() )
print( 'revcomp : ',my_seq.reverse_complement() )
print(f'GC content: {gc_content:.2f}%')
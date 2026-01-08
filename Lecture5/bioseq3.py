from Bio.Seq import Seq
#from Bio.Alphabet import IUPAC

#messenger_rna = Seq("AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG", IUPAC.unambiguous_rna)
messenger_rna = Seq("AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG")

print( messenger_rna )
print( messenger_rna.translate() )

# Now, you may want to translate the nucleotides up to the first in frame stop codon, 
# and then stop (as happens in nature):
print( messenger_rna.translate(to_stop=True) )



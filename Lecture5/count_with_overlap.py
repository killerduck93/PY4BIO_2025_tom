from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

def count_with_overlap(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count

my_seq = Seq("AAAA", IUPAC.unambiguous_dna)

print(count_with_overlap(my_seq, "AA"))

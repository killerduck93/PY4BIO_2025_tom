import string

def revcomp(seq): 
    translation = str.maketrans("agct", "tcga")
    comp = seq.translate(translation)
    rcomp = comp[::-1] # reversing comp
    return rcomp

dna = "cggcgt"
rev = revcomp(dna)
print("Revcomp of %s is %s"%(dna, rev))

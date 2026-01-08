import string

class DNA:
    def __init__(self, sequence):
        self.seq = sequence.lower()
    def revcomp(self):
        translation = str.maketrans("agct", "tcga")
        comp = self.seq.translate(translation)
        self.revcomp = comp[::-1]
    def report(self):
        print ("Revcomp of %s is %s"% (self.seq,self.revcomp))


dna = DNA("accggcatg")# Creating a DNA object
dna.revcomp()
dna.report()

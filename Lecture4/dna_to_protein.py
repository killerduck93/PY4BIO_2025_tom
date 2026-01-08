import sys
from aa import codon_table  # Assuming aa.py contains a dictionary named codon_table

def translate(dna):
    length = len(dna)
    protein = []
    
    for i in range(0, length, 3):
        codon = dna[i:i+3]
        if codon in codon_table:
            protein.append(codon_table[codon])
        else:
            protein.append('?')  # Use '?' for unknown codons
    
    return ''.join(protein)

# Example usage
if __name__ == "__main__":
    print("gatgacgaaagttgt")
    print(translate("gatgacgaaagttgt"))

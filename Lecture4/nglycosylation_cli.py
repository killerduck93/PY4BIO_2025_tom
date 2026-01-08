import sys
import re

if not len(sys.argv) == 2:
        sys.stderr.write("USAGE: python3 %s < protein file (Fasta) >\n" % sys.argv[0])
        sys.exit(1)

protein_file = sys.argv[1]
try:
    with open(protein_file) as f:
        pass
except FileNotFoundError:
    print("File does not exist or is not accessible!!!")
    sys.exit(1)


def read_fasta(infile):
    with open(infile) as f:
        line = f.readline()

        # Double-check that it's a FASTA file by looking for the '>'.
        if not line.startswith(">"):
            raise TypeError("Not a FASTA file: %r" % line)

        # Remove trailing whitespace...
        title = line[1:].rstrip()

        sequence_lines = []
        while 1:
                line = f.readline().rstrip()
                if line == "":
                    # Reached the end of the record or end of the file
                    break
                sequence_lines.append(line)

    # Merge the lines together to make a single string containing the sequence
    sequence = "".join(sequence_lines)

    return (title, sequence)


def find_nglyco(sequence):
    for match in re.finditer("N[^P][ST]", sequence):
        print("Potential N-glycosylation sequence %s at residue %d"%(match.group(), match.start() + 1))


(title, sequence) = read_fasta(protein_file)
print(">"+title)
print(sequence)
find_nglyco(sequence)

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment

align1 = MultipleSeqAlignment([
    SeqRecord(Seq("ACTGCTAGCTAG"), id="Alpha"),
    SeqRecord(Seq("ACT-CTAGCTAG"), id="Beta"),
    SeqRecord(Seq("ACTGCTAGDTAG"), id="Gamma"), ])

from Bio import AlignIO

AlignIO.write(align1, "my_example.phy", "phylip")

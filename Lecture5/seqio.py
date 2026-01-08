import os
from Bio import SeqIO

## save the sequence records to a list
allSeqRecords = []
allSeqIDs     = []
# fasta file is in current directory
pathToFile = os.path.join("./","multi_fasta_gb_header.fasta")
for seq_record in SeqIO.parse(pathToFile, "fasta"):
    allSeqRecords.append(seq_record)
    allSeqIDs.append(seq_record.id.split("|")[1])
    print( seq_record.id )
    # print 1st 10 nucleotides only
    print( str(seq_record.seq[:10]) )
    print( len(seq_record) )

## print out fun stuff about the sequences
print( "We found ", len(allSeqIDs), "sequences" )
print( "information on the third sequence:" )
ind = 2
seqRec = allSeqRecords[ind]
print( "\t", "GI number     ", allSeqIDs[ind] )
print( "\t", "full id       ", seqRec.id )
print( "\t", "num nucleo.   ", len(seqRec.seq) )
print( "\t", "1st 10 nucleo.", seqRec.seq[:10] )

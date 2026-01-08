def count_nmers(seq, n): 
    freq={}
    seq = seq.lower()
    for i in range(len(seq)-n+1):
        nmer=seq[i : i+n]
        if nmer in freq:
            freq[nmer]+=1 # incr. according counter
        else: freq[nmer]=1 # first occurence
    return freq

freq = count_nmers("gatgatgatgatgacgaaagttgt", 3)
for residue in freq.keys():
    print(residue,":", freq[residue])

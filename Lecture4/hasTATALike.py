import re
def hasTataLike(string):
    if (re.search("TATAA[ACGT][ACGT][ACGT]TT", string)):
    #if (re.search("(Fred)*", string)):
        return True
    return False


s = "ACGACGTTTACACGGATATAAGGGTTACGCGCTGTATAATGTGATCAGCTGATTCGAA"
print (hasTataLike(s))
s = "ACGACGTTTACACGGAAATAAGGGTTACGCGCTGTATAATGTGATCAGCTGATTCGAA"
print (hasTataLike(s))

import re


def multipleTataLike(string):
    if (re.search("(TATAA[ACGT]{3}TT).*(TATAA[ACGT]{3}TT)",string)):
        return True
    return False


s = "GATATAAGGGTTACGCGCTATAAGGGTTTTTTTGTATAATGTGATCAGCTGATTCGAA"
print (multipleTataLike(s))
s = "ACGACGTTTACACGGAAATAAGGGTTACGCGCTGTATAATGTGATCAGCTGATTCGAA"
print (multipleTataLike(s))

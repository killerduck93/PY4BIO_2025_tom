import re
pattern = re.compile('[ACGT]')
if pattern.match("A"): print("Matched")
if pattern.match("a"): print("Matched")

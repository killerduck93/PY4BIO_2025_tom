import re

# Step a: Read the file
with open('nuc_sequence.txt', 'r') as file:
    lines = file.readlines()

# Step b: Convert list of lines to a single string
s = ''.join(lines)

# Step c: Convert to uppercase
s = s.upper()

# Step d: Remove newline characters
s = s.replace('\n', '')

# Step 1: Find all substrings with three or more consecutive 'A's
pattern_A = re.compile(r'A{3,}')
matches_A = pattern_A.finditer(s)

print("Substrings with three or more consecutive 'A's:")
for match in matches_A:
    print(f"Match: {match.group()}, Span: {match.span()}")

# Step 2: Find all substrings that start with 'T', followed by two or three 'C's, and end with 'G'
pattern_TCCG = re.compile(r'TCC{2,3}G')
matches_TCCG = pattern_TCCG.finditer(s)

print("\nSubstrings that start with 'T', followed by two or three 'C's, and end with 'G':")
for match in matches_TCCG:
    print(f"Match: {match.group()}, Span: {match.span()}")
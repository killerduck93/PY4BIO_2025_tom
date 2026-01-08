name = ''
sequence = ''
length = 0
with open('fly3utr.txt', 'r') as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('>'):
            if name: # Empty str is False
               print(name, length,'bp')
               print(sequence)
            name = line
            #name = line[1:]
            length = 0
            sequence = ""
        else:
            length += len(line)
            sequence += line
print(name, length, 'bp')
print(sequence)
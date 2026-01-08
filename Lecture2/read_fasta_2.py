name = ''
with open('fly3utr.txt', 'r') as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('>'):
            if name: # Empty str is False
               print(name, length)
            name = line[1:]
            length = 0
        else:
            length += len(line)
print(name, length)

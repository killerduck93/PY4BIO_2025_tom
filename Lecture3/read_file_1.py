f = open('sequence.txt', 'r')
for line in f:
    if not line.startswith('#'):
        print(line.rstrip())
f.close()

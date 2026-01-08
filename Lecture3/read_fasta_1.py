with open('fly3utr.txt', 'r') as f:
    for line in f:
        if line.startswith('>'):
            print(line[1:].rstrip())

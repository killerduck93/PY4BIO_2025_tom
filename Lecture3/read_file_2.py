with open('sequence.txt', 'r') as f:
    for line in f:
        if not line.startswith('#'):
            print( line.rstrip() )

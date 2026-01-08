f3 = open("sequence.txt", "r") 
for line in f3 : 
    if line[-1] == '\n' :
        print(line[:-1])  # remove last char
    else :
        print(line)
f3.close() # not required

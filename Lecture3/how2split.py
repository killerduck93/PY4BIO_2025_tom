f5 = open("sample.txt", "r")
for line in f5 : 
    words = line.split()
    for each_word in words: 
        print(each_word)
f5.close() # not required

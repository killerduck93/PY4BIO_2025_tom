import pickle
fh = open('asciifile.txt', 'wb')
for k in range(3, 6) :
    mylist = [i for i in range(1,k)]
    print(mylist)
    pickle.dump(mylist, fh, protocol = 0)
fh.close()

fhh = open('asciifile.txt', 'rb')
lists = [ ]    # initializing list of lists
while 1 : 
    try: 
        lists.append(pickle.load(fhh))
    except EOFError :
        break
fhh.close()
print(lists)

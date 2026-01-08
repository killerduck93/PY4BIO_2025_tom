def read_file(filename): 
    phonebook = {}
    with open(filename, "r") as f: 
        for line in f.readlines()[1:]:
            name, lastname, number=line.strip().split("\t")
            phonebook[name]=number
        return phonebook

print( read_file("list.csv") )

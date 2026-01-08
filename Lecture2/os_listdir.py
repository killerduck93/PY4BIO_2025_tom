import os

# Current directory
directory = "./"

# Obtain list of files in directory
files = os.listdir(directory)

# Loop over files that end with .txt
for file in files:
    if file.endswith(".txt"):
        f = open(directory + file, "r")
        # do something with file
        print( f.readline().rstrip() )
        f.close()


# betterconvert2csv.py
""" Convert tab-separated file to csv
"""
fh = open('grades.txt','r')    #input file
linelist = [ ]    # global data structure

for line in fh :   # outer loop
    itemlist = line.split('\t')
    # print(str(itemlist)) # just for debugging
    linestring = '' # start afresh
    for item in itemlist :   #inner loop
        item = item.replace('"','""') # for quotes
        if item[-1] == '\n' :   # remove it
             item = item[:-1]
        if ',' in item :       # wrap item
             linestring += '"' + item +'"' + ','
        else :                  # just append
             linestring += item   +','

        # end of inside for loop

    # must replace last comma by newline
    linestring = linestring[:-1] + '\n'
    linelist.append(linestring)
    # end of outside for loop

fh.close()
fhh = open('great.csv', 'w')
for line in linelist :
     fhh.write(line)
fhh.close()

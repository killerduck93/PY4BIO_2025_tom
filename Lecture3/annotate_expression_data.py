DEBUG = False

annotations_file = 'annotation.txt'
annotations_list = [line.rstrip('\n') for line in open(annotations_file)]
# get rid of header line
annotations_list.pop(0)

data_file = 'data.txt'
data_list = [line.rstrip('\n') for line in open(data_file)]

# build annotation dict
lookup_annotation = {}
for line in annotations_list:
    key,value = line.split('\t',1)
    
    if DEBUG:
        print("key: ",key,"\tvalue: ",value)
        
    lookup_annotation[ key ] = value
    
uniq_refseqs = set()

# do the annotation
for line in data_list:
        line_list = line.split('\t')
        
        try:
            annotation = lookup_annotation[line_list[0]]
        except KeyError:
            annotation = "None"
        
        if annotation != "None":
            uniq_refseqs.add(line_list[0])

# Iterating using for loop 
for refseq in uniq_refseqs: 
    print(refseq,'\t',lookup_annotation[refseq]) 

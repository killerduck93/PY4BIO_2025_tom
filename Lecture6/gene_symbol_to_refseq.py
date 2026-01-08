from urllib import request
from os import sys

# https://www.ncbi.nlm.nih.gov/nuccore/?term=(SMAD3%5BAll+Fields%5D+AND+srcdb_refseq%5BPROP%5D)+AND+%22Homo+sapiens%22%5Bporgn%5D
def get_refseq_page(gene_symbol):
    url    = "https://www.ncbi.nlm.nih.gov/nuccore/"
    params = "term=(" + gene_symbol + "%5BAll+Fields%5D+AND+srcdb_refseq%5BPROP%5D)+AND+%22Homo+sapiens%22%5Bporgn%5D"
    fullurl= url + "?" + params

    #print(fullurl)

    result = request.urlopen(fullurl).read()
    result = str(result, encoding='utf-8')
    
    if(result != ''):
        return(result)
    else:
        sys.stderr.write("Nothing was returned\n")

    return("")

refseq_page = get_refseq_page("SMAD3")
print(refseq_page)


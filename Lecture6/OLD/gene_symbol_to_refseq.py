from urllib import request
from os import sys

def get_refseq_page(gene_symbol):
    url    = "https://www.ncbi.nlm.nih.gov/gene/"
    params = "term=" + gene_symbol
    fullurl= url + "?" + params

    result = request.urlopen(fullurl).read()
    result = str(result, encoding='utf-8')
    
    if(result != ''):
        return(result)
    else:
        sys.stderr.write("Nothing was returned\n")

    return("")

refseq_page = get_refseq_page("SMAD3")
print(refseq_page)


from urllib import request
import re
import sys

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

def parse_refseq_page(web_page):
    result =""
    html_lines = web_page.splitlines()
    for line in html_lines: 
        if re.search(r'[A-Z][A-Z]_\d+',line):
            result = re.search(r'[A-Z][A-Z]_\d+',line)
    return(result.group(0))

gene_symbol = "SMAD3"
web_page = get_refseq_page(gene_symbol)
result=parse_refseq_page(web_page)
print("%s: %s" % (gene_symbol, result))

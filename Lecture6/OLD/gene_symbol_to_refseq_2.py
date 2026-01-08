from urllib import request
import re
import sys

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

def parse_refseq_page(web_page):
    result=""
    html_lines = web_page.splitlines()
    for line in html_lines: 
        if re.search(r'<a href="https://www.ncbi.nlm.nih.gov/nuccore/(.*)" id="gene_refseqtranscripts"',line):
            result = re.search(r'<a href="https://www.ncbi.nlm.nih.gov/nuccore/(.*)" id="gene_refseqtranscripts"',line).group(1)
    return(result)

gene_symbol = "SMAD3"
web_page = get_refseq_page(gene_symbol)
result=parse_refseq_page(web_page)
print("%s: %s" % (gene_symbol, result))

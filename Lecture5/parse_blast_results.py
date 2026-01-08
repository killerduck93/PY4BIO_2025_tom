from Bio.Blast import NCBIXML
# open the file directly using python open method and use NCBIXML parse method

E_VALUE_THRESH = 1e-20
for record in NCBIXML.parse(open("insulin.xml")):
    if record.alignments:
        print("\n")
        print("query: %s" % record.query[:100])
        for align in record.alignments:
            for hsp in align.hsps:
                if hsp.expect < E_VALUE_THRESH:
                    print("match: %s " % align.title[:100])



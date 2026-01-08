from Bio.Blast import NCBIWWW
from Bio import SearchIO
from Bio import SeqIO

base_dir = "./"
inputs = ['insulin']

for input in inputs:
    blast_xml = base_dir + input + '.xml'
    blast_out = base_dir + input + '.fa'

    # run BLAST
    fasta_string = open(base_dir + input + '.fasta').read()
    with NCBIWWW.qblast("blastn", "nr", fasta_string) as result_handle:
        with open(blast_xml, 'w') as xml_file:
            xml_file.write(result_handle.read())

    # parse xml and write to fasta
    blast_qresult = SearchIO.read(blast_xml, 'blast-xml')
    records = []
    for hit in blast_qresult:
        records.append(hit[0].hit)
    SeqIO.write(records, blast_out, "fasta")

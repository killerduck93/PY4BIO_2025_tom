from Bio import SeqIO
from Bio.SeqUtils import ProtParam
import sys
import re

ambiguous_AA_regexp = re.compile(r'[XBZJ]')  # to identify sequences with ambiguous AA symbols (X:any,B:DN,Z:EQ,J:IL)


def prot_fasta_IEP_MW( multi_fasta_file, ambiguous_AA_regexp, verbous = 0 ):
    """Parse a multi-FASTA protein file and compute IEP and MW for unambiguous sequences.

    Parameters
    ----------
    multi_fasta_file : str
        Path to a multi-FASTA file containing protein sequences.
    ambiguous_AA_regexp : re.Pattern
        Compiled regular expression that matches ambiguous amino-acid symbols
        (e.g., 'X', 'B', 'Z', 'J'). Sequences matching this pattern are skipped.
    verbous : int, optional
        If non-zero, print a tab-separated line (description, IEP, MW) for each
        processed sequence. Default is 0 (no printing).

    Returns
    -------
    list
        A list of [description, IEP, MW] for each processed (unambiguous) sequence.
    """

    id_IEP_MW_table = []

    # Use a context manager to ensure the file handle is properly closed
    with open(multi_fasta_file) as handle:
        # Iterate over each FASTA record in the file
        for record in SeqIO.parse(handle, "fasta"):
            seq = str(record.seq)

            # Skip sequences that contain ambiguous amino-acid symbols
            if not ambiguous_AA_regexp.search(seq):
                # Analyze sequence properties using Bio.SeqUtils.ProtParam
                X = ProtParam.ProteinAnalysis(seq)

                # Compute isoelectric point (IEP) and molecular weight (MW)
                IEP = X.isoelectric_point()
                MW = X.molecular_weight()

                # Optionally print results in a human-readable tab-separated format
                if verbous:
                    print("%s\t%.2f\t%.1f" % (record.description, IEP, MW))

                # Store result as [description, IEP, MW]
                id_IEP_MW_table.append([record.description, IEP, MW])

    # Return list of results (unchanged behavior)
    return( id_IEP_MW_table )


def retrieve_matching_proteins(id_IEP_MW_table, iep_lower_limit, iep_upper_limit, mw_lower_limit, mw_upper_limit):
    for result in id_IEP_MW_table:
        if iep_lower_limit <= result[1] <= iep_upper_limit:
            if mw_lower_limit  <= result[2] <= mw_upper_limit:
                print("%s\t%.2f\t%.1f" % (result[0], result[1], result[2]))


if __name__ == '__main__':

    if not len(sys.argv) == 5:
        sys.stderr.write("USAGE: python3 %s < IEP lower limit (pH) > < IEP upper limit (pH) > < MW lower limit (Da) > < MW upper limit (Da) >\n" % sys.argv[0])
        sys.exit(1)

    multi_fasta_file = 'uniprot-all.fasta'

    iep_lower_limit = float(sys.argv[1])
    iep_upper_limit = float(sys.argv[2])
    mw_lower_limit = float(sys.argv[3])
    mw_upper_limit = float(sys.argv[4])

    id_IEP_MW_table = []
    try:
        id_IEP_MW_table = prot_fasta_IEP_MW(multi_fasta_file, ambiguous_AA_regexp, verbous=0)
    except FileNotFoundError:
        print(multi_fasta_file, " not existing or not readable! Check please...")

    retrieve_matching_proteins(id_IEP_MW_table, iep_lower_limit, iep_upper_limit, mw_lower_limit, mw_upper_limit)


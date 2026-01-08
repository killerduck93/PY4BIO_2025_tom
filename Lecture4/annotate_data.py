#!/usr/bin/env python3

"""
annotate_data.py
=================

Purpose
-------
Annotate a whitespace-delimited data table by replacing the first field of each
row with one or more annotation columns looked up from a tab-separated (TSV)
annotations file.

Synopsis
--------
        python3 annotate_data.py <annotations.tsv> <data.txt> > annotated.tsv

Inputs
------
1) Annotations file (TSV, required header):
     - The first column is the key (e.g., probe/transcript ID).
     - Remaining columns are the annotation payload. The script stores all columns
         after the first as a single tab-joined string and uses that to replace the
         key in the output.

2) Data file (whitespace-delimited):
     - First field is the lookup key; remaining fields are preserved.

Output
------
Writes annotated rows to standard output, tab-delimited. If a key isn't found
in the annotations, the original first field is preserved.

Behavioral notes
----------------
- The annotations file must have a header line; it is ignored.
- The script stops reading the data file at the first blank line (interpreted as
    end of record). Lines after a blank line are not processed.
- Duplicate keys in the annotations file: the last one wins silently.

Exit codes
----------
- 0 on success
- 1 on incorrect arguments or file access errors

Examples
--------
        python3 annotate_data.py annotations.tsv data.txt > annotated.tsv
        python3 annotate_data.py annotations.tsv data.txt

Limitations (current implementation)
------------------------------------
- Assumes tabs in the annotations file and generic whitespace in the data file.
- Malformed annotation lines without a tab will cause a runtime error.
- No explicit encoding handling (uses system default).

"""

import sys

if not len(sys.argv) == 3:
    sys.stderr.write("USAGE: python3 %s <annotations file> <data file>\n" % sys.argv[0])
    sys.exit(1)

annots_file = sys.argv[1]
data_file = sys.argv[2]

try:
    with open(annots_file) as f:
        pass
    with open(data_file) as f:
        pass
except FileNotFoundError:
    print("File(s) do(es) not exist or is not accessible!!!")
    sys.exit(1)

def construct_lookup_dict(annots_file):
    """Build a lookup dictionary from a TSV annotations file.

    The file is expected to be tab-separated with a header on the first line.
    The first column is treated as the key; all remaining columns (joined by the
    first tab split) are preserved as the value string. The value may itself
    contain tabs if the annotations have multiple columns.

    Args:
        annots_file (str): Path to the annotations TSV file with a header.

    Returns:
        dict[str, str]: Mapping from key (first column) to the remaining columns
                        as a single tab-joined string.

    Notes:
        - If duplicate keys occur, the last occurrence overrides earlier ones.
        - Lines without a tab will raise a ValueError during split.
    """
    annotations_list = [line.rstrip('\n') for line in open(annots_file)]

    # get rid of header line
    annotations_list.pop(0)

    # build annotation dict
    lookup_annotation = {}
    for line in annotations_list:
        key,value = line.split('\t',1)
        lookup_annotation[ key ] = value

    return lookup_annotation

def annotate_data_file(data_file, lookup_annotation):
     """Stream and annotate the data file row by row.

     Reads the data file line by line, splitting on generic whitespace. If the
     first field exists in the lookup dictionary, it is replaced by the
     corresponding annotation string (which may include tabs, i.e., multiple
     columns). The final row is emitted as tab-delimited text.

     Importantly, the current implementation stops processing at the first blank
     line encountered; any subsequent lines are ignored.

     Args:
         data_file (str): Path to the whitespace-delimited data file.
         lookup_annotation (dict[str, str]): Mapping from key to annotations
             payload created by `construct_lookup_dict`.
     """
     with open(data_file) as f:
        while 1:
            line = f.readline().strip()
            if line == "":
                # Reached the end of the record or end of the file
                break

            fields = line.split()
            if lookup_annotation.get(fields[0],0):
                #print(fields[0], lookup_annotation[fields[0]])
                fields[0] = lookup_annotation[fields[0]]

            print('\t'.join(fields))


lookup_annotation = construct_lookup_dict(annots_file)
annotate_data_file(data_file, lookup_annotation)

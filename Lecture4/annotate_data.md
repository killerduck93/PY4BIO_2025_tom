# annotate_data.py — Documentation

## Overview

`annotate_data.py` annotates a tab/whitespace-delimited data table by replacing the first column (an identifier) with one or more annotation columns from a lookup table. It reads:

- an annotations file (TSV with a header), used to construct an in-memory lookup dictionary keyed by the first column, and
- a data file (space/tab-delimited), where each row’s first field is looked up and, if found, replaced by the corresponding annotation fields.

Output is written to standard output, preserving the remainder of the data row and inserting the annotation fields in place of the original first field.

## Quick usage

```bash
python3 annotate_data.py <annotations.tsv> <data.txt> > annotated_output.tsv
```

- `<annotations.tsv>`: tab-separated file with a header on the first line; the first column is the key, subsequent columns are the annotation payload.
- `<data.txt>`: whitespace-delimited file; the first field in each row is the key to be annotated.

Exit codes:
- `0` on success
- `1` on wrong number of arguments or file access errors

## Input specifications

### 1) Annotations file (TSV)

- Required header on the first line (it is ignored by the script).
- Must be tab-separated.
- The first column is the lookup key (e.g., probe ID, transcript ID).
- Remaining columns (joined by tabs) are the annotation payload that replaces the key in the output.

Example `annotations.tsv`:

```
id	gene_name	symbol	desc
P001	Breast cancer type 1 susceptibility protein	BRCA1	Human BRCA1
P002	Tumor protein p53	TP53	Human TP53
```

### 2) Data file (whitespace-delimited)

- Parsed using generic whitespace splitting (spaces and/or tabs).
- The first field is the key used for lookup in the annotations dictionary.
- Remaining fields are preserved as-is.

Example `data.txt`:

```
P001	12.3	7.1	9.9
P002 8.0  6.4  5.2
P999	1.2	3.4	5.6
```

## Output format

- Each input data line is rewritten as:
  `[annotation columns (from annotations.tsv)] + [tab] + [original data fields 2..N]`
- If a key is not found in the annotations, the original first field is preserved.
- Lines are joined with tabs in the output. Note that the annotation payload can itself contain tabs (multiple columns), which the script emits intact.

Given the inputs above, the output would look like:

```
Breast cancer type 1 susceptibility protein	BRCA1	Human BRCA1	12.3	7.1	9.9
Tumor protein p53	TP53	Human TP53	8.0	6.4	5.2
P999	1.2	3.4	5.6
```

## How it works (implementation notes)

- Validates exactly two arguments: annotations file and data file. On mismatch, prints usage to stderr and exits with code 1.
- Checks both files are accessible; if not, prints an error and exits with code 1.
- Builds `lookup_annotation` by:
  - Reading all lines of the annotations file, stripping trailing newlines.
  - Removing the first line (header) via `pop(0)`.
  - Splitting each remaining line into `key` and `value` using the first tab only (`split('\t', 1)`).
  - Storing `lookup_annotation[key] = value` (where `value` may contain embedded tabs, i.e., multiple columns).
- Reads the data file line by line, splitting each non-empty line on whitespace (`split()`).
- If `fields[0]` exists as a key in `lookup_annotation`, replaces `fields[0]` with the full `value` string (possibly multi-column). The final print uses `\t`.join(fields), preserving any tabs inside the replaced value.

## Contract

- Inputs:
  - `annotations.tsv`: TSV with header; at least two tab-separated columns per non-header line.
  - `data.txt`: whitespace-delimited; at least one field per non-empty line.
- Output: Annotated rows to stdout, tab-delimited; stderr is used for the usage message.
- Side effects: None (pure file I/O and stdout writes).
- Performance: O(A + D) time, where A = number of annotation rows and D = number of data rows; memory O(U) for unique annotation keys.

## Examples

Annotate `data.txt` with `annotations.tsv` and save the result:

```bash
python3 annotate_data.py annotations.tsv data.txt > annotated.tsv
```

Stream to screen:

```bash
python3 annotate_data.py annotations.tsv data.txt
```

## Assumptions and limitations

- The annotations file must be tab-separated and contain a header line; the first data line will be dropped if no header is present.
- The script stops processing when it encounters an empty line in the data file (interpreted as “end of record”); any lines after the first blank line are ignored.
- Duplicate keys in the annotations file: the last occurrence silently overrides earlier ones.
- Malformed annotation lines without a tab will cause a runtime error.
- Data lines with only one field are allowed; they will be annotated if the key is found.
- Encoding is assumed to be the system default; no explicit encoding is set.

## Troubleshooting

- “USAGE … < annotations file > < data file >” printed to stderr: supply exactly two file paths.
- “File(s) do(es) not exist or is not accessible!!!”: check file paths and permissions.
- Output seems truncated: ensure there are no blank lines in `data.txt`; the first blank line stops processing.
- No annotations applied: verify the first field in the data matches the first column in the annotations (exact string match), and that the annotations file is tab-separated.

## Suggested improvements (optional)

While not part of the current behavior, the following small changes would improve robustness:

- Iterate over lines with `for line in f:` and explicitly `continue` on blank lines, rather than `break`, to avoid early termination.
- Accept a `--no-header` option for annotations files without headers.
- Add `--delimiter` parameters for both files to support custom separators.
- Use `argparse` for clearer CLI and `--help` documentation.
- Validate and report malformed lines rather than crashing on split errors.

## File reference

- Script: `Lecture4/annotate_data.py`
- This documentation: `Lecture4/annotate_data.md`

---
Last updated: 2025-10-15

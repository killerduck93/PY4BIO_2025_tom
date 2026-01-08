#!/usr/bin/env python3
"""
Filter microarray-like tabular data by log2 thresholds.

Rules (both must be true to keep a row):
1) log2(SampleA) > 2 OR log2(SampleB) > 2
2) |log2(SampleA) - log2(SampleB)| > 3

Usage:
    python filter_microarray.py raw_data.txt filtered_data.txt

Notes:
- The input is expected to be a delimited text file (TSV/CSV). The delimiter is auto-detected.
- The first line is treated as header and preserved in the output.
- Rows with non-positive values (<= 0) in SampleA/SampleB are skipped (log2 undefined).
- If headers differ (e.g., 'Sample A data'/'Sample B data'), try passing --sampleA and --sampleB to set column names.
"""
from __future__ import annotations
import csv
import math
import sys
import argparse

def detect_dialect_and_header(path: str):
    # Read a sample to sniff delimiter
    with open(path, "r", newline="") as f:
        sample = f.read(1024 * 64)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters="\t,;| ")
        except csv.Error:
            # default to tab if detection fails
            dialect = csv.excel_tab
        # Detect header presence (assume yes)
        has_header = True
    return dialect, has_header

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Filter microarray data by log2 criteria.")
    p.add_argument("input", help="Input data file (TSV/CSV with header).")
    p.add_argument("output", help="Output file for filtered rows.")
    p.add_argument("--sampleA", default=None, help="Column name for Sample A (default: auto-detect 'SampleA' or 'Sample A data').")
    p.add_argument("--sampleB", default=None, help="Column name for Sample B (default: auto-detect 'SampleB' or 'Sample B data').")
    return p.parse_args(argv)

def choose_sample_columns(fieldnames, colA_opt, colB_opt):
    # Preferred names
    candidatesA = [colA_opt, "SampleA", "Sample A", "Sample A data"]
    candidatesB = [colB_opt, "SampleB", "Sample B", "Sample B data"]
    def pick(cands):
        for c in cands:
            if c and c in fieldnames:
                return c
        # fallback: last two numeric-looking columns? here, just raise
        return None
    colA = pick(candidatesA)
    colB = pick(candidatesB)
    if not colA or not colB:
        raise SystemExit(f"Could not find sample columns in header. Available columns: {fieldnames}")
    return colA, colB

def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None

def keep_row(a, b):
    # Skip rows with invalid or non-positive values
    if a is None or b is None or a <= 0.0 or b <= 0.0:
        return False, None, None
    la = math.log2(a)
    lb = math.log2(b)
    cond1 = (la > 2.0) or (lb > 2.0)
    cond2 = abs(la - lb) > 3.0
    return (cond1 and cond2), la, lb

def main(argv=None):
    args = parse_args(argv)
    dialect, _ = detect_dialect_and_header(args.input)

    with open(args.input, "r", newline="") as fin:
        reader = csv.DictReader(fin, dialect=dialect)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise SystemExit("No header detected in input file.")
        colA, colB = choose_sample_columns(fieldnames, args.sampleA, args.sampleB)

        with open(args.output, "w", newline="") as fout:
            writer = csv.DictWriter(fout, fieldnames=fieldnames, dialect=dialect)
            writer.writeheader()

            total = 0
            kept = 0
            skipped_nonpos = 0
            for row in reader:
                total += 1
                a = safe_float(row[colA])
                b = safe_float(row[colB])
                keep, la, lb = keep_row(a, b)
                if a is None or b is None or (a is not None and a <= 0.0) or (b is not None and b <= 0.0):
                    skipped_nonpos += 1
                if keep:
                    writer.writerow(row)
                    kept += 1

    # Print a short report to stdout
    print(f"Processed rows (excluding header): {total}")
    print(f"Kept rows: {kept}")
    if skipped_nonpos:
        print(f"Skipped due to non-positive/invalid values: {skipped_nonpos}")

if __name__ == "__main__":
    main()

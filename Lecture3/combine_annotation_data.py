#!/usr/bin/env python3
"""
Combine RefSeq accessions, data values, and descriptions.

Inputs (default):
  - annotation.txt: Tab-separated file with header: "RefSeq DNA ID\tDescription"
  - data.txt: Tab-separated file with rows: accession followed by numeric values

Output:
  - combined_data_with_annotations.tsv: accession, all data columns, description

Sanity checks performed:
  - Skip empty lines and header lines (e.g., lines starting with "RefSeq DNA ID")
  - Validate annotation lines have accession and description
  - Validate data lines have accession and at least one numeric datapoint
  - Verify each accession in data exists in annotation before writing
  - Report counts of total/merged/skipped lines with reasons

Usage:
  python combine_annotation_data.py \
      --annotations annotation.txt \
      --data data.txt \
      --output combined_data_with_annotations.tsv

All paths are relative to the current working directory unless absolute.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def is_accession(token: str) -> bool:
    """Return True if token looks like a RefSeq accession of interest (NM_/NR_)."""
    if not token:
        return False
    # Common RefSeq mRNA (NM_), non-coding (NR_), and others could exist (e.g., XM_, XR_)
    return token.startswith(("NM_", "NR_", "XM_", "XR_"))


def read_annotations(path: Path) -> Dict[str, str]:
    lookup: Dict[str, str] = {}
    skipped_header = False
    bad_lines = 0
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter="\t")
        for row_idx, row in enumerate(reader, start=1):
            if not row:
                continue
            if row_idx == 1 and row[0].strip().lower().startswith("refseq dna id"):
                skipped_header = True
                continue
            # Expect at least 2 columns: accession, description (description can include tabs, so join rest)
            if len(row) < 2:
                bad_lines += 1
                continue
            acc = row[0].strip()
            desc = "\t".join(row[1:]).strip()
            if not acc or not desc:
                bad_lines += 1
                continue
            lookup[acc] = desc
    if not lookup:
        raise SystemExit(f"No annotations parsed from {path}; header_skipped={skipped_header}, bad_lines={bad_lines}")
    return lookup


def parse_numeric_values(values: List[str]) -> Tuple[bool, List[str]]:
    """Check that all values are numeric (int/float). Return (ok, normalized_str_values)."""
    normalized: List[str] = []
    for v in values:
        s = v.strip()
        if s == "":
            return False, []
        # Allow integers and floats; we keep as original strings to preserve formatting
        try:
            # Try int, then float; but don't change representation in output
            int(s)
        except ValueError:
            try:
                float(s)
            except ValueError:
                return False, []
        normalized.append(s)
    return True, normalized


def read_data_rows(path: Path) -> List[Tuple[str, List[str], int]]:
    rows: List[Tuple[str, List[str], int]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if not parts:
                continue
            acc = parts[0].strip()
            # Skip header or malformed first column
            if acc.lower().startswith("refseq dna id") or not acc:
                continue
            if not is_accession(acc):
                # Not a recognizable accession; skip noisily
                # But allow numeric-only first column? No — treat as bad
                continue
            values = parts[1:]
            if len(values) == 0:
                # require at least one data value
                continue
            ok, norm_values = parse_numeric_values(values)
            if not ok:
                continue
            rows.append((acc, norm_values, line_no))
    return rows


def write_output(path: Path, merged_rows: List[Tuple[str, List[str], str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        # header
        header = ["Accession"]
        if merged_rows:
            # Use number of data columns from first row
            header.extend([f"Value{i+1}" for i in range(len(merged_rows[0][1]))])
        header.append("Description")
        writer.writerow(header)
        for acc, values, desc in merged_rows:
            writer.writerow([acc, *values, desc])


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Combine data values with annotations by RefSeq accession")
    ap.add_argument("--annotations", "-a", default="annotation.txt", help="Path to annotation TSV (default: annotation.txt)")
    ap.add_argument("--data", "-d", default="data.txt", help="Path to data TSV (default: data.txt)")
    ap.add_argument("--output", "-o", default="combined_data_with_annotations.tsv", help="Output TSV path")
    args = ap.parse_args(argv)

    ann_path = Path(args.annotations)
    data_path = Path(args.data)
    out_path = Path(args.output)

    if not ann_path.exists():
        print(f"ERROR: Annotations file not found: {ann_path}", file=sys.stderr)
        return 2
    if not data_path.exists():
        print(f"ERROR: Data file not found: {data_path}", file=sys.stderr)
        return 2

    annotations = read_annotations(ann_path)
    data_rows = read_data_rows(data_path)

    total_rows = len(data_rows)
    merged_rows: List[Tuple[str, List[str], str]] = []
    missing_annotation = 0
    for acc, values, _line_no in data_rows:
        desc = annotations.get(acc)
        if desc is None or desc.strip() == "":
            missing_annotation += 1
            continue
        merged_rows.append((acc, values, desc))

    write_output(out_path, merged_rows)

    # Report summary to stderr
    print(
        (
            f"Done. Read {total_rows} data rows. "
            f"Merged: {len(merged_rows)}. "
            f"Skipped (missing annotation): {missing_annotation}. "
            f"Output: {out_path}"
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

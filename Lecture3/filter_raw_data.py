#!/usr/bin/env python3
"""
Filter a tab-separated expression dataset by log2 thresholds.

Input:  raw_data.txt-like file with header. Expected columns include SampleA and SampleB
        (header names are flexible: e.g., 'SampleA', 'Sample A', 'Sample A data', 'Sample_B', etc.).

Rules:
  - Keep header unchanged.
  - For each data row, compute log2 of SampleA and SampleB.
  - Keep the row only if both conditions hold:
      1) max(log2A, log2B) > 2
      2) abs(log2A - log2B) > 3
  - Rows with non-numeric or non-positive values in SampleA/B are skipped (log2 undefined).

Usage:
  python filter_raw_data.py [input_path] [output_path]
  Defaults: input_path=./raw_data.txt (in same folder), output_path=./filtered_data.txt
"""

from __future__ import annotations

import csv
import math
import os
import sys
from typing import List, Tuple


def read_text_with_fallbacks(path: str) -> Tuple[List[str], str]:
    """Read text file lines trying multiple encodings. Returns (lines, encoding).

    Tries: utf-8, utf-8-sig, latin-1.
    """
    encodings = ["utf-8", "utf-8-sig", "latin-1"]
    last_err: Exception | None = None
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                # Read all lines to surface any decode problems now
                return f.readlines(), enc
        except Exception as e:  # UnicodeDecodeError or others
            last_err = e
            continue
    # If all failed, re-raise last error
    raise RuntimeError(f"Failed to read '{path}' with encodings {encodings}: {last_err}")


def normalize_header_name(name: str) -> str:
    # Lowercase, strip, collapse spaces/underscores
    n = name.strip().lower().replace("_", " ")
    # Remove double spaces
    n = " ".join(n.split())
    return n


def find_sample_columns(header: List[str]) -> Tuple[int, int]:
    """Return indices for SampleA and SampleB columns from header names.

    Supports variants like:
      - 'samplea', 'sample a', 'sample a data', 'sample a value'
      - 'sampleb', 'sample b', 'sample b data', 'sample b value'
    """
    normalized = [normalize_header_name(h) for h in header]

    candidates_a = {
        "samplea",
        "sample a",
        "sample a data",
        "sample a value",
        "sample a values",
    }
    candidates_b = {
        "sampleb",
        "sample b",
        "sample b data",
        "sample b value",
        "sample b values",
    }

    idx_a = idx_b = -1
    for i, n in enumerate(normalized):
        if n in candidates_a and idx_a == -1:
            idx_a = i
        if n in candidates_b and idx_b == -1:
            idx_b = i

    # Common compact headers like 'samplea'/'sampleb' without spaces are already covered

    if idx_a == -1 or idx_b == -1:
        # Try exact case-sensitive fallback (as in provided example: 'SampleA', 'SampleB')
        try:
            idx_a = header.index("SampleA") if idx_a == -1 else idx_a
        except ValueError:
            pass
        try:
            idx_b = header.index("SampleB") if idx_b == -1 else idx_b
        except ValueError:
            pass

    if idx_a == -1 or idx_b == -1:
        raise ValueError(
            f"Could not find both SampleA and SampleB columns in header: {header}"
        )
    return idx_a, idx_b


def parse_float_safe(value: str) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def row_passes(a: float, b: float) -> bool:
    # log2 only defined for positive values
    if a <= 0 or b <= 0:
        return False
    log2a = math.log2(a)
    log2b = math.log2(b)
    cond1 = max(log2a, log2b) > 2
    cond2 = abs(log2a - log2b) > 3
    return cond1 and cond2


def filter_file(input_path: str, output_path: str) -> Tuple[int, int]:
    """Filter input_path and write rows to output_path. Returns (total_rows, kept_rows)."""
    text_lines, used_encoding = read_text_with_fallbacks(input_path)

    # Use csv reader with tab delimiter on the already-read lines
    reader = csv.reader(text_lines, delimiter="\t")
    rows = list(reader)
    if not rows:
        raise ValueError(f"Input file '{input_path}' appears to be empty.")

    header = rows[0]
    if len(header) < 2:
        raise ValueError(
            f"Header seems malformed (fewer than 2 columns): {header} from file {input_path}"
        )
    try:
        idx_a, idx_b = find_sample_columns(header)
    except ValueError as e:
        # If standard detection fails, assume last two columns are SampleA and SampleB (common layout)
        if len(header) >= 2:
            idx_a, idx_b = len(header) - 2, len(header) - 1
        else:
            raise e

    kept: List[List[str]] = [header]
    total = 0
    kept_count = 0
    for row in rows[1:]:
        if not row or all(c.strip() == "" for c in row):
            continue
        total += 1
        # Some TSV writers might have split fewer columns if trailing tabs are missing; pad safely
        if len(row) <= max(idx_a, idx_b):
            # Skip malformed rows
            continue
        a_val = parse_float_safe(row[idx_a])
        b_val = parse_float_safe(row[idx_b])
        if a_val is None or b_val is None:
            continue
        if row_passes(a_val, b_val):
            kept.append(row)
            kept_count += 1

    # Write output using the same delimiter and a consistent encoding (utf-8)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(kept)

    return total, kept_count


def main(argv: List[str]) -> int:
    # Default paths: same folder as script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_in = os.path.join(script_dir, "raw_data.txt")
    default_out = os.path.join(script_dir, "filtered_data.txt")

    input_path = argv[1] if len(argv) > 1 else default_in
    output_path = argv[2] if len(argv) > 2 else default_out

    try:
        total, kept = filter_file(input_path, output_path)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    print(
        f"Read {total} data rows from '{input_path}' and kept {kept} rows. Output -> '{output_path}'"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

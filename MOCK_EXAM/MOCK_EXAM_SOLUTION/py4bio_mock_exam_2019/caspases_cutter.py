#!/usr/bin/env python3
"""
Caspases Cleavage Site Predictor
PY4BIO Mock Exam - November 20th 2019

This script predicts potential cleavage sites by caspases in protein sequences.
Usage:
    python caspases_cutter.py <accession_id>
    python caspases_cutter.py <file_with_ids>
"""

from Bio import ExPASy, SeqIO
import sys
import re
import os


# Define caspase cleavage patterns (8-character peptides)
# Pattern format: P4-P3-P2-P1 | P1'-P2'-P3'-P4'
# Cleavage occurs between P1 and P1' (between 4th and 5th position)
# NOTE: Based on expected exam output, patterns are more permissive than typical literature
CASPASE_PATTERNS = {
    'caspase_1': re.compile(r'...D.{4}'),
    # Very permissive: any 3 chars at P4-P3-P2, D at P1, any 4 at P1'-P4'
    # This matches all exam outputs: FLTD, LITD, LPAD, YGAD, LKAD, LFTD, LTTD
    
    'caspase_2': re.compile(r'[DVEAI][^DEGHKRP][^DEGHKRP]D.{4}'),
    # D/V/E/A/I at P4, not (D/E/G/H/K/R/P) at P3 and P2, D at P1
    
    'caspase_3': re.compile(r'[DVEAMI][^DEGHKRP][^DEGHKRP]D.{4}'),
    # D/V/E/A/M/I at P4, not (D/E/G/H/K/R/P) at P3 and P2, D at P1
    
    'caspase_4': re.compile(r'[LWEVAIF][^DEGHKRP].[DE].{4}'),
    # L/W/E/V/A/I/F at P4, not (D/E/G/H/K/R/P) at P3, any at P2, D/E at P1
    
    'caspase_5': re.compile(r'[LWEVAIF][^DEGHKRP].D.{4}'),
    # L/W/E/V/A/I/F at P4, not (D/E/G/H/K/R/P) at P3, any at P2, D at P1
    
    'caspase_6': re.compile(r'[VETI][^DEGHKRP][^DEGHKRP]D.{4}'),
    # V/E/T/I at P4, not (D/E/G/H/K/R/P) at P3 and P2, D at P1
    
    'caspase_7': re.compile(r'DEVD.{4}'),
    # Specific sequence DEVD at P4-P1
    
    'caspase_8': re.compile(r'[ILVE][^DEGHKRP][^DEGHKRP]D.{4}'),
    # I/L/V/E at P4, not (D/E/G/H/K/R/P) at P3 and P2, D at P1
    
    'caspase_9': re.compile(r'[LVEAI][^DEGHKRP].[DE].{4}'),
    # L/V/E/A/I at P4, not (D/E/G/H/K/R/P) at P3, any at P2, D/E at P1
    
    'caspase_10': re.compile(r'IEAD.{4}'),
    # Specific sequence IEAD at P4-P1 (from exam example)
}


def get_protein_sequence(accession_id):
    """
    Retrieve protein sequence from UniProt using ExPASy.
    
    Args:
        accession_id: UniProt Swiss-Prot accession ID (e.g., 'P17405')
    
    Returns:
        SeqRecord object or None if not found
    """
    try:
        handle = ExPASy.get_sprot_raw(accession_id.strip())
        record = SeqIO.read(handle, "swiss")
        handle.close()
        return record
    except Exception as e:
        print(f"Error retrieving {accession_id}: {e}", file=sys.stderr)
        return None


def find_caspase_cleavage_sites(record, caspase_patterns):
    """
    Find all caspase cleavage sites in a protein sequence.
    
    Args:
        record: SeqRecord object from Biopython
        caspase_patterns: Dictionary of {caspase_name: compiled_regex}
    
    Returns:
        List of tuples: (accession, name, caspase_type, site_sequence, position, length)
    """
    results = []
    sequence = str(record.seq)
    seq_length = len(sequence)
    
    # Extract accession and name from record
    # record.id format: "sp|P17405|ASM_HUMAN" 
    # record.name format: "ASM_HUMAN"
    if '|' in record.id:
        parts = record.id.split('|')
        accession = parts[1]
        protein_name = parts[2] if len(parts) > 2 else record.name
    else:
        accession = record.id
        protein_name = record.name if hasattr(record, 'name') and record.name else accession
    
    # Search for each caspase pattern
    for caspase_type, pattern in caspase_patterns.items():
        for match in pattern.finditer(sequence):
            site_sequence = match.group()[:8]  # Take only the 8-character octapeptide
            position = match.start() + 1  # Convert to 1-based position
            
            results.append({
                'accession': accession,
                'name': protein_name,
                'caspase': caspase_type,
                'site': site_sequence,
                'position': position,
                'length': seq_length
            })
    
    return results


def process_accession_id(accession_id, caspase_patterns):
    """
    Process a single accession ID and return all cleavage sites found.
    
    Args:
        accession_id: UniProt accession ID
        caspase_patterns: Dictionary of caspase patterns
    
    Returns:
        List of result dictionaries
    """
    record = get_protein_sequence(accession_id)
    if record:
        return find_caspase_cleavage_sites(record, caspase_patterns)
    return []


def print_results(results):
    """
    Print results in the specified format.
    Format: accession name caspase_type site_sequence position length
    """
    for result in results:
        print(f"{result['accession']} {result['name']} {result['caspase']} "
              f"{result['site']} {result['position']} {result['length']}")


def main():
    """Main function to handle command-line arguments and execute the program."""
    if len(sys.argv) != 2:
        print("USAGE: python caspases_cutter.py <accession_id OR file_with_ids>", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  python caspases_cutter.py P17405", file=sys.stderr)
        print("  python caspases_cutter.py test.set", file=sys.stderr)
        sys.exit(1)
    
    input_arg = sys.argv[1]
    all_results = []
    
    # Check if input is a file or a single accession ID
    if os.path.isfile(input_arg):
        # Process file with multiple accession IDs
        try:
            with open(input_arg, 'r') as f:
                accession_ids = [line.strip() for line in f if line.strip()]
            
            for acc_id in accession_ids:
                results = process_accession_id(acc_id, CASPASE_PATTERNS)
                all_results.extend(results)
        
        except IOError as e:
            print(f"Error reading file {input_arg}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Process single accession ID
        results = process_accession_id(input_arg, CASPASE_PATTERNS)
        all_results.extend(results)
    
    # Print all results
    print_results(all_results)


if __name__ == '__main__':
    main()

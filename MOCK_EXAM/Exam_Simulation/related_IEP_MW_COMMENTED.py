#!/usr/bin/env python3
"""
LEVEL 1: COMMAND-LINE INTERFACE
================================

This script implements all three requirements:
(1) Calculates isoelectric point (IEP) for each protein
(2) Calculates molecular weight (MW) for each protein  
(3) Returns entries matching the specified criteria using AND logic

File: related_IEP_MW.py
Purpose: Standalone command-line tool to search UniProtKB database
"""

import sys
from pathlib import Path

# Import BioPython's protein analysis module
# This provides IEP and MW calculation algorithms
try:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
except ImportError:
    print("Error: BioPython is not installed. Please install it with: pip install biopython")
    sys.exit(1)


# ============================================================================
# FUNCTION 1: Read FASTA File
# ============================================================================
def read_fasta(fasta_file):
    """
    REQUIREMENT: Support reading from UniProtKB FASTA database
    
    Read a FASTA file and yield (header, sequence) tuples.
    
    Args:
        fasta_file: Path to the FASTA file
        
    Yields:
        Tuples of (header, sequence) where:
        - header: UniProtKB identifier line (e.g., "sp|O75503|CLN5_HUMAN...")
        - sequence: amino acid sequence string
    
    Implementation:
    - Streams file for memory efficiency (uses generator)
    - Handles empty lines gracefully
    - Accumulates multi-line sequences until next '>' marker
    """
    header = None
    sequence = []
    
    try:
        with open(fasta_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith('>'):
                    # Yield previous sequence if it exists
                    if header is not None:
                        yield header, ''.join(sequence)
                    header = line[1:]  # Remove '>' character
                    sequence = []
                else:
                    sequence.append(line)
            
            # Don't forget the last sequence
            if header is not None:
                yield header, ''.join(sequence)
    except FileNotFoundError:
        print(f"Error: File '{fasta_file}' not found.")
        sys.exit(1)


# ============================================================================
# FUNCTION 2: Calculate IEP and MW
# IMPLEMENTS REQUIREMENTS (1) AND (2)
# ============================================================================
def calculate_iep_mw(sequence):
    """
    REQUIREMENT (1): Calculate isoelectric point (IEP) for a protein
    REQUIREMENT (2): Calculate molecular weight (MW) for a protein
    
    This function uses BioPython's ProteinAnalysis class which implements:
    - IEP: Bjellqvist et al. (1994) algorithm
    - MW: Sums atomic weights of all atoms in the sequence
    
    Args:
        sequence: Amino acid sequence as string (IUPAC standard codes)
        
    Returns:
        Tuple of (IEP, MW) where:
        - IEP (float): pH value where protein has zero net charge (3.0 - 13.0 range)
        - MW (float): Molecular weight in Daltons
        
        Returns (None, None) if calculation fails (invalid sequence)
    
    Examples:
        "MVDREQLVQKAKLAEQAERYYDDMAAAMKAVTELNEPLSNEERNLLSVAYKNVVGARRSSW..."
        → IEP: 7.04, MW: 41496.1
    """
    try:
        # Create ProteinAnalysis object
        # This parses the amino acid sequence and calculates properties
        pa = ProteinAnalysis(sequence)
        
        # Calculate isoelectric point (pH where net charge = 0)
        iep = pa.isoelectric_point()
        
        # Calculate molecular weight (sum of all atomic masses minus water)
        mw = pa.molecular_weight()
        
        return iep, mw
    except Exception as e:
        # Handle invalid sequences gracefully (skip them)
        return None, None


# ============================================================================
# FUNCTION 3: Main Function - Handle CLI and Filtering
# IMPLEMENTS REQUIREMENT (3): Filter by criteria (AND logic)
# ============================================================================
def main():
    """
    REQUIREMENT (3): Return all entries satisfying the specified conditions
    
    This is the main entry point that:
    1. Validates command-line arguments
    2. Shows usage statement if no arguments provided
    3. Reads FASTA file
    4. Calculates IEP/MW for all proteins (Requirements 1 & 2)
    5. Filters using AND logic: (IEP_min ≤ IEP ≤ IEP_max) AND (MW_min ≤ MW ≤ MW_max)
    6. Outputs matching proteins in specified format
    
    Command-line format:
        python3 related_IEP_MW.py <iep_lower> <iep_upper> <mw_lower> <mw_upper>
    
    Examples:
        python3 related_IEP_MW.py 7 7.1 41000 42000
        → Returns proteins with 7.0-7.1 pH and 41000-42000 Da
    """
    
    # ---- Argument Validation ----
    if len(sys.argv) != 5:
        # Display usage when invoked without correct number of arguments
        print("USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> <IEP upper limit (pH)> <MW lower limit (Da)> <MW upper limit (Da)>")
        print("\nExample: python3 related_IEP_MW.py 7 7.1 41000 42000")
        sys.exit(1)
    
    # ---- Parse command-line arguments ----
    try:
        iep_lower = float(sys.argv[1])  # Minimum IEP (pH)
        iep_upper = float(sys.argv[2])  # Maximum IEP (pH)
        mw_lower = float(sys.argv[3])   # Minimum MW (Daltons)
        mw_upper = float(sys.argv[4])   # Maximum MW (Daltons)
    except ValueError:
        print("Error: All arguments must be numeric values.")
        print("USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> <IEP upper limit (pH)> <MW lower limit (Da)> <MW upper limit (Da)>")
        sys.exit(1)
    
    # ---- Locate the FASTA database file ----
    script_dir = Path(__file__).parent
    fasta_file = script_dir.parent / "MOCK_EXAM" / "MOCK_EXAM_SOLUTION" / "CGI" / "uniprot-all.fasta"
    
    if not fasta_file.exists():
        print(f"Error: FASTA file not found at {fasta_file}")
        sys.exit(1)
    
    # ---- Process FASTA file and filter proteins ----
    matching_proteins = []
    
    # Iterate through all proteins in the database
    for header, sequence in read_fasta(str(fasta_file)):
        # REQUIREMENT (1) & (2): Calculate IEP and MW for this protein
        iep, mw = calculate_iep_mw(sequence)
        
        # Skip if calculation failed (invalid sequence)
        if iep is None or mw is None:
            continue
        
        # REQUIREMENT (3): Apply AND logic filtering
        # Only include if BOTH conditions are satisfied:
        # - IEP is within the specified range
        # - MW is within the specified range
        if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
            matching_proteins.append((header, iep, mw))
    
    # ---- Output Results ----
    # Display matching proteins in the specified format:
    # <UniProt_ID> <Description> <IEP> <MW>
    for header, iep, mw in matching_proteins:
        print(f"{header} {iep:.2f} {mw:.1f}")
    
    # If no matches found, inform user
    if not matching_proteins:
        print(f"No proteins found matching criteria: {iep_lower} <= IEP <= {iep_upper} AND {mw_lower} <= MW <= {mw_upper}")


# ============================================================================
# Entry Point
# ============================================================================
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
================================================================================
SOLUZIONE LEVEL 1 - ASSIGNMENT: Protein IEP and MW Calculator
================================================================================

REQUISITI ASSIGNMENT (da TestGuideline2025.txt):
------------------------------------------------
(1) Calcola il punto isoelettrico (IEP) per ogni sequenza proteica
(2) Calcola il peso molecolare (MW) per ogni sequenza proteica
(3) Restituisce tutte le entry che soddisfano le condizioni specificate
    alla riga di comando con logica AND: 
    8.5 <= IEP <= 8.7 AND 44000 <= MW <= 45000

COMPORTAMENTO RICHIESTO:
------------------------
- Senza argomenti: mostra messaggio di usage
- Con argomenti: stampa le proteine che soddisfano i criteri

ESEMPIO OUTPUT ATTESO:
----------------------
python related_IEP_MW.py 7 7.1 41000 42000
sp|O75503|CLN5_HUMAN Ceroid-lipofuscinosis neuronal protein 5 OS=Homo sapiens GN=CLN5 PE=1 SV=2 7.04 41496.1
sp|Q9NZJ6|COQ3_HUMAN Ubiquinone biosynthesis O-methyltransferase, mitochondrial OS=Homo sapiens GN=COQ3 PE=1 SV=3 7.10 41053.6

DOCUMENTAZIONE BIOPYTHON:
-------------------------
- Bio.SeqUtils.ProtParam.ProteinAnalysis: 
  https://biopython.org/wiki/ProtParam
- isoelectric_point(): calcola il pH al quale la proteina ha carica netta zero
- molecular_weight(): calcola il peso molecolare in Daltons

File: related_IEP_MW.py
Autore: Soluzione Assignment PY4BIO 2025
"""

import sys
from pathlib import Path

# ============================================================================
# IMPORT BIOPYTHON - REQUISITO FONDAMENTALE
# ============================================================================
# BioPython fornisce algoritmi scientificamente validati per:
# - Calcolo del punto isoelettrico (metodo di Bjellqvist et al., 1994)
# - Calcolo del peso molecolare (somma dei pesi atomici degli amminoacidi)
# Documentazione: https://biopython.org/wiki/ProtParam
try:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
except ImportError:
    print("Error: BioPython is not installed. Please install it with: pip install biopython")
    sys.exit(1)


def read_fasta(fasta_file):
    """
    Read a FASTA file and yield (header, sequence) tuples.
    
    Args:
        fasta_file: Path to the FASTA file
        
    Yields:
        Tuples of (header, sequence)
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


def calculate_iep_mw(sequence):
    """
    Calculate isoelectric point (IEP) and molecular weight (MW) of a protein sequence.
    
    Args:
        sequence: Amino acid sequence as string
        
    Returns:
        Tuple of (IEP, MW) or (None, None) if calculation fails
    """
    try:
        # Create ProteinAnalysis object
        pa = ProteinAnalysis(sequence)
        
        # Calculate properties
        iep = pa.isoelectric_point()
        mw = pa.molecular_weight()
        
        return iep, mw
    except Exception as e:
        # Handle invalid sequences gracefully
        return None, None


def main():
    """Main function to process command-line arguments and filter proteins."""
    
    # Check usage
    if len(sys.argv) != 5:
        print("USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> <IEP upper limit (pH)> <MW lower limit (Da)> <MW upper limit (Da)>")
        print("\nExample: python3 related_IEP_MW.py 7 7.1 41000 42000")
        sys.exit(1)
    
    # Parse command-line arguments
    try:
        iep_lower = float(sys.argv[1])
        iep_upper = float(sys.argv[2])
        mw_lower = float(sys.argv[3])
        mw_upper = float(sys.argv[4])
    except ValueError:
        print("Error: All arguments must be numeric values.")
        print("USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> <IEP upper limit (pH)> <MW lower limit (Da)> <MW upper limit (Da)>")
        sys.exit(1)
    
    # Locate the FASTA file
    # The script is in Exam_Simulation folder, FASTA is in MOCK_EXAM_SOLUTION/CGI
    # Path structure: MOCK_EXAM/Exam_Simulation/related_IEP_MW.py
    #                -> MOCK_EXAM/MOCK_EXAM_SOLUTION/CGI/uniprot-all.fasta
    script_dir = Path(__file__).parent
    fasta_file = script_dir.parent / "MOCK_EXAM_SOLUTION" / "CGI" / "uniprot-all.fasta"
    
    if not fasta_file.exists():
        print(f"Error: FASTA file not found at {fasta_file}")
        sys.exit(1)
    
    # Process FASTA file
    matching_proteins = []
    
    for header, sequence in read_fasta(str(fasta_file)):
        iep, mw = calculate_iep_mw(sequence)
        
        # Skip if calculation failed
        if iep is None or mw is None:
            continue
        
        # Check if protein matches criteria
        if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
            matching_proteins.append((header, iep, mw))
    
    # Display results
    for header, iep, mw in matching_proteins:
        print(f"{header} {iep:.2f} {mw:.1f}")
    
    # Print summary if no matches found
    if not matching_proteins:
        print(f"No proteins found matching criteria: {iep_lower} <= IEP <= {iep_upper} AND {mw_lower} <= MW <= {mw_upper}")


if __name__ == "__main__":
    main()

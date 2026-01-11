#!/usr/bin/env python3
"""
LEVEL 2 (BOSS LEVEL): WEB CGI INTERFACE
========================================

This script implements a web-based interface to the protein search tool.
It reuses the same calculation logic from LEVEL 1 but serves results via HTML.

REQUIREMENTS IMPLEMENTED:
- Build a Python CGI web interface to the tool
- Display proteins satisfying the requested conditions
- Provide HTML form for parameter input
- Show results in a formatted table

File: related_IEP_MW.cgi
Purpose: CGI backend to handle web requests and return HTML results
"""

import cgi
import cgitb
import os
import sys
from pathlib import Path

# Enable CGI error reporting for debugging
cgitb.enable()

# Import BioPython's protein analysis module
# This is the SAME module used in LEVEL 1
try:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
except ImportError:
    pass


# ============================================================================
# FUNCTION 1: Read FASTA File (Same as LEVEL 1)
# ============================================================================
def read_fasta(fasta_file):
    """
    Read a FASTA file and yield (header, sequence) tuples.
    This function is IDENTICAL to LEVEL 1 for consistency.
    
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
                    if header is not None:
                        yield header, ''.join(sequence)
                    header = line[1:]
                    sequence = []
                else:
                    sequence.append(line)
            
            if header is not None:
                yield header, ''.join(sequence)
    except FileNotFoundError:
        pass


# ============================================================================
# FUNCTION 2: Calculate IEP and MW (Same as LEVEL 1)
# IMPLEMENTS REQUIREMENTS (1) AND (2)
# ============================================================================
def calculate_iep_mw(sequence):
    """
    REQUIREMENT (1): Calculate isoelectric point (IEP)
    REQUIREMENT (2): Calculate molecular weight (MW)
    
    This function is IDENTICAL to LEVEL 1.
    It uses BioPython's ProteinAnalysis to compute protein properties.
    
    Returns:
        Tuple of (IEP, MW) or (None, None) if invalid sequence
    """
    try:
        pa = ProteinAnalysis(sequence)
        iep = pa.isoelectric_point()
        mw = pa.molecular_weight()
        return iep, mw
    except Exception as e:
        return None, None


# ============================================================================
# FUNCTION 3: Find Matching Proteins
# IMPLEMENTS REQUIREMENT (3): Filter by criteria (AND logic)
# ============================================================================
def find_matching_proteins(iep_lower, iep_upper, mw_lower, mw_upper, fasta_file):
    """
    REQUIREMENT (3): Return all entries matching specified criteria
    
    This function uses the SAME AND logic as LEVEL 1:
    (IEP_min ≤ IEP ≤ IEP_max) AND (MW_min ≤ MW ≤ MW_max)
    
    Args:
        iep_lower: Minimum IEP value (pH)
        iep_upper: Maximum IEP value (pH)
        mw_lower: Minimum MW value (Daltons)
        mw_upper: Maximum MW value (Daltons)
        fasta_file: Path to FASTA database
    
    Returns:
        List of tuples (header, iep, mw) for matching proteins
    """
    matching_proteins = []
    
    # Iterate through database
    for header, sequence in read_fasta(fasta_file):
        # Calculate IEP and MW (Requirements 1 & 2)
        iep, mw = calculate_iep_mw(sequence)
        
        # Skip invalid sequences
        if iep is None or mw is None:
            continue
        
        # Apply AND logic filtering (Requirement 3)
        if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
            matching_proteins.append((header, iep, mw))
    
    return matching_proteins


# ============================================================================
# FUNCTION 4: Escape HTML Special Characters
# ============================================================================
def escape_html(text):
    """
    Escape HTML special characters for safe display.
    Prevents XSS (Cross-Site Scripting) attacks.
    
    Returns:
        Safe HTML string
    """
    return (text.replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;")
               .replace('"', "&quot;")
               .replace("'", "&#39;"))


# ============================================================================
# FUNCTION 5: Generate and Output HTML
# MAIN CGI HANDLER
# ============================================================================
def main():
    """
    MAIN CGI HANDLER FUNCTION
    
    This function:
    1. Prints HTTP headers
    2. Parses form data from user input
    3. Calls find_matching_proteins() (which implements Requirements 1,2,3)
    4. Generates HTML page with results
    
    Flow:
    - User submits HTML form with IEP/MW criteria
    - This function receives form data
    - Searches database for matching proteins
    - Returns results as HTML table
    """
    
    # ---- Print HTTP Header ----
    # Required by CGI protocol to indicate HTML response
    print("Content-Type: text/html; charset=utf-8")
    print()
    
    # ---- Parse Form Data ----
    # Extract parameters from HTML form submission
    form = cgi.FieldStorage()
    
    # Initialize default values
    iep_lower_val = ""
    iep_upper_val = ""
    mw_lower_val = ""
    mw_upper_val = ""
    results_html = ""
    
    # ---- Check if form was submitted with search criteria ----
    if "iep_lower" in form and "iep_upper" in form and "mw_lower" in form and "mw_upper" in form:
        try:
            # Parse numeric values from form
            iep_lower = float(form.getvalue("iep_lower"))
            iep_upper = float(form.getvalue("iep_upper"))
            mw_lower = float(form.getvalue("mw_lower"))
            mw_upper = float(form.getvalue("mw_upper"))
            
            # Store for form field repopulation
            iep_lower_val = str(iep_lower)
            iep_upper_val = str(iep_upper)
            mw_lower_val = str(mw_lower)
            mw_upper_val = str(mw_upper)
            
            # ---- Locate FASTA database ----
            script_dir = Path(__file__).parent
            fasta_file = script_dir.parent / "uniprot-all.fasta"
            
            # Alternative path if above doesn't work
            if not fasta_file.exists():
                fasta_file = Path("c:\\Users\\march\\PY4BIO_2025\\MOCK_EXAM\\MOCK_EXAM_SOLUTION\\CGI\\uniprot-all.fasta")
            
            # ---- Check if FASTA file exists ----
            if fasta_file.exists():
                # REQUIREMENTS (1), (2), (3) implemented here
                matching_proteins = find_matching_proteins(
                    iep_lower, iep_upper, mw_lower, mw_upper, str(fasta_file)
                )
                
                # ---- Generate HTML results table ----
                if matching_proteins:
                    # Proteins found - show results in table
                    results_html = f"""
            <div class="results-section">
                <h2>Search Results</h2>
                <div class="results-info">
                    Found <strong>{len(matching_proteins)}</strong> matching protein(s) for:
                    {iep_lower:.2f} &le; IEP &le; {iep_upper:.2f} AND {mw_lower:.0f} &le; MW &le; {mw_upper:.0f}
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>UniProt ID</th>
                            <th>Protein Description</th>
                            <th>IEP (pH)</th>
                            <th>MW (Da)</th>
                        </tr>
                    </thead>
                    <tbody>
"""
                    # Add each matching protein as a table row
                    for header, iep, mw in matching_proteins:
                        uniprot_id = escape_html(header.split()[0])
                        full_desc = escape_html(header)
                        results_html += f"""                        <tr>
                            <td><strong>{uniprot_id}</strong></td>
                            <td>{full_desc}</td>
                            <td>{iep:.2f}</td>
                            <td>{mw:.1f}</td>
                        </tr>
"""
                    results_html += """                    </tbody>
                </table>
            </div>
"""
                else:
                    # No proteins matching criteria
                    results_html = f"""
            <div class="results-section">
                <div class="no-results">
                    No proteins found matching the criteria: {iep_lower:.2f} &le; IEP &le; {iep_upper:.2f} AND {mw_lower:.0f} &le; MW &le; {mw_upper:.0f}
                </div>
            </div>
"""
            else:
                # FASTA file not found
                results_html = """
            <div class="results-section">
                <div class="error-message">
                    Error: FASTA database file not found. Please check the server configuration.
                </div>
            </div>
"""
        except ValueError:
            # Invalid numeric input
            results_html = """
            <div class="results-section">
                <div class="error-message">
                    Error: Please enter valid numeric values for all fields.
                </div>
            </div>
"""
    
    # ---- Print Complete HTML Page ----
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Protein IEP and MW Search</title>
    <style>
        body {{
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .form-section {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}
        
        .form-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #555;
        }}
        
        .form-group input {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1em;
        }}
        
        button {{
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
        }}
        
        .btn-search {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 100%;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
        }}
        
        table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        
        .error-message {{
            background: #ffebee;
            color: #d32f2f;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #d32f2f;
        }}
        
        .results-info {{
            background: #e7f3ff;
            color: #0066cc;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
            border-left: 4px solid #0066cc;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 Protein Database Search</h1>
            <p>Search UniProtKB for proteins by Isoelectric Point and Molecular Weight</p>
        </div>
        
        <div class="content">
            <form method="POST" class="search-form">
                <div class="form-section">
                    <h2>Search Criteria</h2>
                    
                    <h3>Isoelectric Point (pH) Range</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="iep_lower">Lower Limit (pH)</label>
                            <input type="number" id="iep_lower" name="iep_lower" step="0.1" 
                                   placeholder="e.g., 7.0" value="{iep_lower_val}">
                        </div>
                        <div class="form-group">
                            <label for="iep_upper">Upper Limit (pH)</label>
                            <input type="number" id="iep_upper" name="iep_upper" step="0.1" 
                                   placeholder="e.g., 7.5" value="{iep_upper_val}">
                        </div>
                    </div>
                    
                    <h3>Molecular Weight (Da) Range</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="mw_lower">Lower Limit (Da)</label>
                            <input type="number" id="mw_lower" name="mw_lower" step="100" 
                                   placeholder="e.g., 41000" value="{mw_lower_val}">
                        </div>
                        <div class="form-group">
                            <label for="mw_upper">Upper Limit (Da)</label>
                            <input type="number" id="mw_upper" name="mw_upper" step="100" 
                                   placeholder="e.g., 42000" value="{mw_upper_val}">
                        </div>
                    </div>
                    
                    <button type="submit" class="btn-search">🔍 Search</button>
                </div>
            </form>
            
            {results_html}
        </div>
        
        <div class="footer">
            <p>Powered by BioPython ProtParam | UniProtKB Human Database</p>
        </div>
    </div>
</body>
</html>"""
    
    print(html_template)


# ============================================================================
# Entry Point
# ============================================================================
if __name__ == "__main__":
    main()

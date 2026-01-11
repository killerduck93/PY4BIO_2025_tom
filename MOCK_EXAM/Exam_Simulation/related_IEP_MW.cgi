#!/usr/bin/env python3
"""
CGI web interface for protein IEP and molecular weight search.

This script provides a web interface to query the UniProtKB database
for proteins matching specific IEP and MW criteria.

To use with a CGI-enabled web server, place this script in the cgi-bin directory
and ensure it has execute permissions.
"""

import cgi
import cgitb
import os
import sys
from pathlib import Path

# Enable CGI error reporting
cgitb.enable()

# Try to import BioPython's ProtParam module
try:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
except ImportError:
    pass


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
        pass


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


def find_matching_proteins(iep_lower, iep_upper, mw_lower, mw_upper, fasta_file):
    """
    Find proteins matching the given criteria.
    
    Returns:
        List of tuples (header, iep, mw) for matching proteins
    """
    matching_proteins = []
    
    for header, sequence in read_fasta(fasta_file):
        iep, mw = calculate_iep_mw(sequence)
        
        # Skip if calculation failed
        if iep is None or mw is None:
            continue
        
        # Check if protein matches criteria
        if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
            matching_proteins.append((header, iep, mw))
    
    return matching_proteins


def escape_html(text):
    """Escape HTML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")


def print_html(iep_lower_val, iep_upper_val, mw_lower_val, mw_upper_val, results_html):
    """Print the complete HTML page."""
    
    # Start HTML document
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Protein IEP and MW Search</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
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
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1.1em;
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
        
        .form-section h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.3em;
        }}
        
        .form-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .form-row.full {{
            grid-template-columns: 1fr;
        }}
        
        .form-group {{
            display: flex;
            flex-direction: column;
        }}
        
        .form-group label {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #555;
            font-size: 0.95em;
        }}
        
        .form-group input {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1em;
            transition: border-color 0.3s;
        }}
        
        .form-group input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.2);
        }}
        
        .form-group-label {{
            font-weight: 600;
            margin-bottom: 15px;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .button-row {{
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }}
        
        button {{
            flex: 1;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .btn-search {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-search:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-reset {{
            background: #e9ecef;
            color: #333;
        }}
        
        .btn-reset:hover {{
            background: #dee2e6;
        }}
        
        .results-section {{
            margin-top: 30px;
        }}
        
        .results-section h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.3em;
        }}
        
        .results-info {{
            background: #e7f3ff;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
            color: #0066cc;
            border-left: 4px solid #0066cc;
        }}
        
        .error-message {{
            background: #ffebee;
            padding: 15px;
            border-radius: 4px;
            color: #d32f2f;
            border-left: 4px solid #d32f2f;
            margin-bottom: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        table thead {{
            background: #667eea;
            color: white;
        }}
        
        table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        
        table tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        table tbody tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.1em;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
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
                    
                    <div class="form-group-label">Isoelectric Point (pH) Range</div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="iep_lower">Lower Limit (pH)</label>
                            <input type="number" id="iep_lower" name="iep_lower" step="0.1" placeholder="e.g., 7.0" value="{iep_lower_val}">
                        </div>
                        <div class="form-group">
                            <label for="iep_upper">Upper Limit (pH)</label>
                            <input type="number" id="iep_upper" name="iep_upper" step="0.1" placeholder="e.g., 7.5" value="{iep_upper_val}">
                        </div>
                    </div>
                    
                    <div class="form-group-label">Molecular Weight (Da) Range</div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="mw_lower">Lower Limit (Da)</label>
                            <input type="number" id="mw_lower" name="mw_lower" step="100" placeholder="e.g., 41000" value="{mw_lower_val}">
                        </div>
                        <div class="form-group">
                            <label for="mw_upper">Upper Limit (Da)</label>
                            <input type="number" id="mw_upper" name="mw_upper" step="100" placeholder="e.g., 42000" value="{mw_upper_val}">
                        </div>
                    </div>
                    
                    <div class="button-row">
                        <button type="submit" class="btn-search">🔍 Search</button>
                        <button type="reset" class="btn-reset">Clear</button>
                    </div>
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
    print(html)


def main():
    """Main CGI handler function."""
    
    # Print HTTP header
    print("Content-Type: text/html; charset=utf-8")
    print()
    
    # Parse form data
    form = cgi.FieldStorage()
    
    # Get form values
    iep_lower_val = ""
    iep_upper_val = ""
    mw_lower_val = ""
    mw_upper_val = ""
    results_html = ""
    
    if "iep_lower" in form and "iep_upper" in form and "mw_lower" in form and "mw_upper" in form:
        try:
            iep_lower = float(form.getvalue("iep_lower"))
            iep_upper = float(form.getvalue("iep_upper"))
            mw_lower = float(form.getvalue("mw_lower"))
            mw_upper = float(form.getvalue("mw_upper"))
            
            iep_lower_val = str(iep_lower)
            iep_upper_val = str(iep_upper)
            mw_lower_val = str(mw_lower)
            mw_upper_val = str(mw_upper)
            
            # Locate the FASTA file
            script_dir = Path(__file__).parent
            fasta_file = script_dir.parent / "MOCK_EXAM" / "MOCK_EXAM_SOLUTION" / "CGI" / "uniprot-all.fasta"
            
            # Alternative path
            if not fasta_file.exists():
                fasta_file = Path("c:\\Users\\march\\PY4BIO_2025\\MOCK_EXAM\\MOCK_EXAM_SOLUTION\\CGI\\uniprot-all.fasta")
            
            if fasta_file.exists():
                matching_proteins = find_matching_proteins(iep_lower, iep_upper, mw_lower, mw_upper, str(fasta_file))
                
                if matching_proteins:
                    results_html = f"""            <div class="results-section">
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
                    results_html = f"""            <div class="results-section">
                <div class="no-results">
                    No proteins found matching the criteria: {iep_lower:.2f} &le; IEP &le; {iep_upper:.2f} AND {mw_lower:.0f} &le; MW &le; {mw_upper:.0f}
                </div>
            </div>
"""
            else:
                results_html = """            <div class="results-section">
                <div class="error-message">
                    Error: FASTA database file not found. Please check the server configuration.
                </div>
            </div>
"""
        except ValueError:
            results_html = """            <div class="results-section">
                <div class="error-message">
                    Error: Please enter valid numeric values for all fields.
                </div>
            </div>
"""
    
    # Print the HTML page
    print_html(iep_lower_val, iep_upper_val, mw_lower_val, mw_upper_val, results_html)


if __name__ == "__main__":
    main()

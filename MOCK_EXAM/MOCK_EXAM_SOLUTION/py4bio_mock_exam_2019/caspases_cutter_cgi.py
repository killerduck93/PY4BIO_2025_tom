#!/usr/bin/env python3
"""
Caspases Cleavage Site Predictor - CGI Interface
PY4BIO Mock Exam - Level 2

CGI web interface for the caspases cutter tool.
"""

import cgi
import cgitb
from Bio import ExPASy, SeqIO
import re

# Enable CGI debugging
cgitb.enable()

# Define caspase cleavage patterns (same as main script)
CASPASE_PATTERNS = {
    'caspase_1': re.compile(r'[FWYL][^DEGHKRP][^DEGHKRP]D.{4}'),
    'caspase_2': re.compile(r'[DVEAI][^DEGHKRP][^DEGHKRP]D.{4}'),
    'caspase_3': re.compile(r'[DVEAMI][^DEGHKRP][^DEGHKRP]D.{4}'),
    'caspase_4': re.compile(r'[LWEVAIF][^DEGHKRP].[DE].{4}'),
    'caspase_5': re.compile(r'[LWEVAIF][^DEGHKRP].D.{4}'),
    'caspase_6': re.compile(r'[VETI][^DEGHKRP][^DEGHKRP]D.{4}'),
    'caspase_7': re.compile(r'DEVD.{4}'),
    'caspase_8': re.compile(r'[ILVE][^DEGHKRP][^DEGHKRP]D.{4}'),
    'caspase_9': re.compile(r'[LVEAI][^DEGHKRP].[DE].{4}'),
    'caspase_10': re.compile(r'IEAD.{4}'),
}


def get_protein_sequence(accession_id):
    """Retrieve protein sequence from UniProt using ExPASy."""
    try:
        handle = ExPASy.get_sprot_raw(accession_id.strip())
        record = SeqIO.read(handle, "swiss")
        handle.close()
        return record
    except Exception:
        return None


def find_caspase_cleavage_sites(record, caspase_patterns):
    """Find all caspase cleavage sites in a protein sequence."""
    results = []
    sequence = str(record.seq)
    seq_length = len(sequence)
    
    # Extract accession and name from record ID
    if '|' in record.id:
        parts = record.id.split('|')
        accession = parts[1]
        protein_name = parts[2] if len(parts) > 2 else record.description.split()[0]
    else:
        accession = record.id
        protein_name = record.description.split()[0] if record.description else "UNKNOWN"
    
    # Search for each caspase pattern
    for caspase_type, pattern in caspase_patterns.items():
        for match in pattern.finditer(sequence):
            site_sequence = match.group()[:8]
            position = match.start() + 1
            
            results.append({
                'accession': accession,
                'name': protein_name,
                'caspase': caspase_type,
                'site': site_sequence,
                'position': position,
                'length': seq_length
            })
    
    return results


def print_results_html(results):
    """Print results as HTML table."""
    if not results:
        print("<p>No cleavage sites found.</p>")
        return
    
    print("<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse;'>")
    print("<tr style='background-color: #4CAF50; color: white;'>")
    print("<th>Accession</th><th>Protein Name</th><th>Caspase Type</th>")
    print("<th>Site Sequence</th><th>Position</th><th>Protein Length</th>")
    print("</tr>")
    
    for i, result in enumerate(results):
        # Alternate row colors for readability
        bg_color = "#f2f2f2" if i % 2 == 0 else "white"
        print(f"<tr style='background-color: {bg_color};'>")
        print(f"<td>{result['accession']}</td>")
        print(f"<td>{result['name']}</td>")
        print(f"<td>{result['caspase']}</td>")
        print(f"<td><code>{result['site']}</code></td>")
        print(f"<td>{result['position']}</td>")
        print(f"<td>{result['length']}</td>")
        print("</tr>")
    
    print("</table>")
    print(f"<p><strong>Total cleavage sites found: {len(results)}</strong></p>")


# Main CGI execution
print('Content-Type: text/html\n')

# Get form data
form = cgi.FieldStorage()
accession_ids_input = form.getvalue('accession_ids', '')

# HTML output
print("""
<!DOCTYPE html>
<html>
<head>
    <title>Caspases Cleavage Site Predictor - Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            margin-top: 20px;
        }
        th {
            font-weight: bold;
            text-align: left;
            padding: 10px;
        }
        td {
            padding: 8px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .back-link {
            margin-top: 20px;
            display: inline-block;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 3px;
        }
        .back-link:hover {
            background-color: #45a049;
        }
        .error {
            color: #d32f2f;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 3px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🧬 Caspases Cleavage Site Predictor - Results</h1>
""")

if accession_ids_input:
    # Process accession IDs
    accession_ids = [aid.strip() for aid in accession_ids_input.split('\n') if aid.strip()]
    
    if accession_ids:
        print(f"<p>Analyzing {len(accession_ids)} protein(s)...</p>")
        
        all_results = []
        errors = []
        
        for acc_id in accession_ids:
            record = get_protein_sequence(acc_id)
            if record:
                results = find_caspase_cleavage_sites(record, CASPASE_PATTERNS)
                all_results.extend(results)
            else:
                errors.append(acc_id)
        
        # Display errors if any
        if errors:
            print("<div class='error'>")
            print(f"<strong>Warning:</strong> Could not retrieve sequences for: {', '.join(errors)}")
            print("</div>")
        
        # Display results
        print_results_html(all_results)
    else:
        print("<div class='error'>No valid accession IDs provided.</div>")
else:
    print("<div class='error'>No accession IDs provided.</div>")

print("""
    <br>
    <a href="javascript:history.back()" class="back-link">← Back to Form</a>
</div>
</body>
</html>
""")

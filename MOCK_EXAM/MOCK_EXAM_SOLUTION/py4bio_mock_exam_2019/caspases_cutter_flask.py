#!/usr/bin/env python3
"""
Caspases Cleavage Site Predictor - Flask Interface
PY4BIO Mock Exam - Flask Alternative

Modern Flask web interface for the caspases cutter tool.
"""

from flask import Flask, render_template, request, render_template_string
import caspases_cutter as CC  # Import the main script as module
import re

app = Flask(__name__)

# HTML template (embedded for simplicity)
FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Caspases Cleavage Site Predictor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .description {
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #4CAF50;
        }
        label {
            display: block;
            margin-top: 20px;
            font-weight: bold;
            color: #555;
        }
        textarea {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ddd;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
        }
        .submit-btn {
            margin-top: 20px;
            padding: 12px 30px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .submit-btn:hover {
            background-color: #45a049;
        }
        .example {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 3px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🧬 Caspases Cleavage Site Predictor</h1>
    
    <div class="description">
        <p><strong>About:</strong> This tool predicts potential cleavage sites by caspases in protein sequences.</p>
    </div>
    
    <form action="/" method="post">
        <label for="accession_ids">
            Enter UniProt Swiss-Prot Accession IDs (one per line):
        </label>
        <textarea 
            id="accession_ids" 
            name="accession_ids" 
            rows="10" 
            placeholder="Enter accession IDs, one per line"
            required>O00238
P17405
Q01814
Q9H3R0
Q9HCP0</textarea>
        
        <button type="submit" class="submit-btn">🔍 Find Cleavage Sites</button>
    </form>
</div>
</body>
</html>
"""

RESULTS_TEMPLATE = """
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
            border-collapse: collapse;
        }
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            text-align: left;
            padding: 10px;
        }
        td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
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
    
    {% if errors %}
    <div class="error">
        <strong>Warning:</strong> Could not retrieve sequences for: {{ ', '.join(errors) }}
    </div>
    {% endif %}
    
    {% if results %}
    <p>Found <strong>{{ results|length }}</strong> cleavage site(s) in {{ num_proteins }} protein(s).</p>
    
    <table>
        <thead>
            <tr>
                <th>Accession</th>
                <th>Protein Name</th>
                <th>Caspase Type</th>
                <th>Site Sequence</th>
                <th>Position</th>
                <th>Protein Length</th>
            </tr>
        </thead>
        <tbody>
            {% for result in results %}
            <tr>
                <td>{{ result.accession }}</td>
                <td>{{ result.name }}</td>
                <td>{{ result.caspase }}</td>
                <td><code>{{ result.site }}</code></td>
                <td>{{ result.position }}</td>
                <td>{{ result.length }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No cleavage sites found.</p>
    {% endif %}
    
    <br>
    <a href="/" class="back-link">← Back to Form</a>
</div>
</body>
</html>
"""


@app.route("/")
def show_form():
    """Display the input form."""
    return render_template_string(FORM_TEMPLATE)


@app.route("/", methods=["POST"])
def show_results():
    """Process the form and display results."""
    accession_ids_input = request.form.get("accession_ids", "")
    accession_ids = [aid.strip() for aid in accession_ids_input.split('\n') if aid.strip()]
    
    all_results = []
    errors = []
    
    if accession_ids:
        for acc_id in accession_ids:
            results = CC.process_accession_id(acc_id, CC.CASPASE_PATTERNS)
            if results:
                all_results.extend(results)
            else:
                errors.append(acc_id)
    
    return render_template_string(
        RESULTS_TEMPLATE,
        results=all_results,
        errors=errors,
        num_proteins=len(accession_ids)
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#!/usr/bin/env python3
"""
Standalone web server for protein IEP and MW search.

This script runs a simple HTTP server that handles both static HTML
and dynamic searches without requiring CGI configuration.

Usage:
    python web_server.py

Then open: http://localhost:8001/
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys
from pathlib import Path
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Server configuration
# Allow overriding PORT via first command-line argument or PORT environment variable
DEFAULT_PORT = int(os.environ.get('PORT', 8001))
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port specified: {sys.argv[1]}; falling back to {DEFAULT_PORT}")
        PORT = DEFAULT_PORT
else:
    PORT = DEFAULT_PORT

SERVER_DIR = Path(__file__).parent
# Correct path: Exam_Simulation -> MOCK_EXAM -> MOCK_EXAM_SOLUTION -> CGI -> uniprot-all.fasta
FASTA_FILE = SERVER_DIR.parent / "MOCK_EXAM_SOLUTION" / "CGI" / "uniprot-all.fasta"

class ProteinSearchHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for protein search."""
    
    # Set the directory to serve files from
    def translate_path(self, path):
        """Override to serve from the current directory."""
        # Get the default translation
        path = super().translate_path(path)
        # For root path, serve index.html
        if os.path.isdir(path):
            if not path.endswith(os.sep):
                path = path + os.sep
            path = os.path.join(path, 'index.html')
        return path
    
    def end_headers(self):
        """Override to add CORS headers to all responses."""
        self.add_cors_headers()
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests - serve static files."""
        if self.path == "/":
            # Serve index.html
            self.path = "/index.html"
        
        if self.path == "/api/search":
            # This shouldn't happen with GET, but handle it anyway
            self.send_response(405)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Method Not Allowed")
            return
        
        # Serve static files (CORS headers added automatically in end_headers)
        try:
            super().do_GET()
        except Exception as e:
            print(f"Error serving GET {self.path}: {e}")
            if not self.headers_sent:
                self.send_error(500, f"Internal Server Error: {e}")
    
    def do_POST(self):
        """Handle POST requests for protein search."""
        if self.path == "/api/search":
            self.handle_search_request()
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()  # CORS headers added automatically
            self.wfile.write(b"Not Found")
    
    def add_cors_headers(self):
        """Add CORS headers to response. Must be called AFTER send_response."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def handle_search_request(self):
        """Process protein search request."""
        try:
            # Read POST data
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(body)
            
            # Extract and convert parameters
            try:
                iep_lower = float(params.get('iep_lower', [''])[0])
                iep_upper = float(params.get('iep_upper', [''])[0])
                mw_lower = float(params.get('mw_lower', [''])[0])
                mw_upper = float(params.get('mw_upper', [''])[0])
            except (ValueError, IndexError):
                self.send_error(400, "Invalid parameters")
                return
            
            # Validate ranges
            if iep_lower > iep_upper or mw_lower > mw_upper:
                response = json.dumps({
                    'success': False,
                    'error': 'Lower limit must be less than or equal to upper limit'
                }).encode('utf-8')
                
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(response))
                self.end_headers()  # CORS headers added automatically
                self.wfile.write(response)
                return
            
            # Search database
            results = self.search_proteins(iep_lower, iep_upper, mw_lower, mw_upper)
            
            # Send response
            response = json.dumps({
                'success': True,
                'count': len(results),
                'results': results
            }).encode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(response))
            self.end_headers()  # CORS headers added automatically
            self.wfile.write(response)
            
        except Exception as e:
            error_response = json.dumps({
                'success': False,
                'error': str(e)
            }).encode('utf-8')
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(error_response))
            self.end_headers()  # CORS headers added automatically
            self.wfile.write(error_response)
    
    def search_proteins(self, iep_lower, iep_upper, mw_lower, mw_upper):
        """Search for proteins matching the criteria."""
        results = []
        count = 0
        
        if not FASTA_FILE.exists():
            raise FileNotFoundError(f"Database not found: {FASTA_FILE}")
        
        try:
            with open(FASTA_FILE, 'r') as f:
                header = None
                sequence = []
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith('>'):
                        # Process previous sequence
                        if header and sequence:
                            seq_str = ''.join(sequence)
                            try:
                                pa = ProteinAnalysis(seq_str)
                                iep = pa.isoelectric_point()
                                mw = pa.molecular_weight()
                                
                                # Check if matches criteria (AND logic)
                                if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
                                    # Extract UniProt ID from header
                                    parts = header.split('|')
                                    uniprot_id = parts[1] if len(parts) > 1 else header
                                    desc = parts[2] if len(parts) > 2 else header
                                    
                                    results.append({
                                        'id': uniprot_id,
                                        'description': desc[:80],  # Truncate long descriptions
                                        'iep': round(iep, 2),
                                        'mw': round(mw, 1)
                                    })
                                    
                                    # Limit results to avoid huge responses
                                    if len(results) >= 100:
                                        break
                            except Exception as e:
                                # Skip sequences that can't be analyzed
                                pass
                        
                        header = line[1:]  # Remove '>'
                        sequence = []
                    else:
                        sequence.append(line)
                
                # Don't forget the last sequence
                if header and sequence and len(results) < 100:
                    seq_str = ''.join(sequence)
                    try:
                        pa = ProteinAnalysis(seq_str)
                        iep = pa.isoelectric_point()
                        mw = pa.molecular_weight()
                        
                        if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
                            parts = header.split('|')
                            uniprot_id = parts[1] if len(parts) > 1 else header
                            desc = parts[2] if len(parts) > 2 else header
                            
                            results.append({
                                'id': uniprot_id,
                                'description': desc[:80],
                                'iep': round(iep, 2),
                                'mw': round(mw, 1)
                            })
                    except Exception as e:
                        pass
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Database not found: {FASTA_FILE}")
        
        return results
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.end_headers()  # CORS headers added automatically

if __name__ == '__main__':
    # Change to server directory
    os.chdir(SERVER_DIR)
    
    # Create socket server
    with socketserver.TCPServer(("", PORT), ProteinSearchHandler) as httpd:
        print(f"")
        print(f"╔═══════════════════════════════════════════════════════════╗")
        print(f"║  Protein Search Server - Running                          ║")
        print(f"╚═══════════════════════════════════════════════════════════╝")
        print(f"")
        print(f"🌐 Open in browser:")
        print(f"   http://localhost:{PORT}/")
        print(f"")
        print(f"📊 Database:")
        print(f"   {FASTA_FILE}")
        print(f"")
        print(f"✓ Server is listening on port {PORT}")
        print(f"⌨️  Press Ctrl+C to stop the server")
        print(f"")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n\nServer stopped.")


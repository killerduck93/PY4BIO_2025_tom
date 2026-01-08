#!/usr/bin/env python3
"""
Script di Test Completo per Caspases Cutter
Verifica funzionalità e correttezza dell'implementazione
"""

import sys
import os
import re

# Colori per output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name, passed, details=""):
    """Stampa risultato di un test"""
    symbol = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
    status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
    print(f"{symbol} {name}: {status}")
    if details:
        print(f"  └─ {details}")

def print_section(title):
    """Stampa header di sezione"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

# TEST 1: Verifica file esistenti
print_section("TEST 1: Verifica File")

files_to_check = [
    'caspases_cutter.py',
    'test.set',
    'caspases_cutter_cgi.py',
    'caspases_form.html',
    'caspases_cutter_flask.py'
]

all_files_exist = True
for filename in files_to_check:
    exists = os.path.isfile(filename)
    print_test(f"File '{filename}' esiste", exists)
    all_files_exist = all_files_exist and exists

if not all_files_exist:
    print(f"\n{RED}ERRORE: Alcuni file mancano. Assicurati di essere nella cartella corretta.{RESET}")
    sys.exit(1)

# TEST 2: Verifica sintassi Python
print_section("TEST 2: Verifica Sintassi Python")

python_files = ['caspases_cutter.py', 'caspases_cutter_cgi.py', 'caspases_cutter_flask.py']

for filename in python_files:
    try:
        with open(filename, 'r') as f:
            compile(f.read(), filename, 'exec')
        print_test(f"Sintassi '{filename}'", True, "Nessun errore di sintassi")
    except SyntaxError as e:
        print_test(f"Sintassi '{filename}'", False, f"Errore: {e}")

# TEST 3: Verifica imports
print_section("TEST 3: Verifica Importazioni")

required_modules = {
    'Bio': 'biopython',
    'flask': 'flask',
    'cgi': 'built-in',
    're': 'built-in',
    'sys': 'built-in'
}

for module, package in required_modules.items():
    try:
        __import__(module)
        print_test(f"Modulo '{module}'", True, f"Installato ({package})")
    except ImportError:
        if package == 'built-in':
            print_test(f"Modulo '{module}'", False, "Modulo built-in non trovato!")
        else:
            print_test(f"Modulo '{module}'", False, f"Installa con: pip install {package}")

# TEST 4: Verifica pattern regex
print_section("TEST 4: Verifica Pattern Regex")

# Import del modulo (se possibile)
try:
    sys.path.insert(0, os.getcwd())
    import caspases_cutter as cc
    
    # Test pattern esistono
    has_patterns = hasattr(cc, 'CASPASE_PATTERNS')
    print_test("CASPASE_PATTERNS definito", has_patterns)
    
    if has_patterns:
        num_patterns = len(cc.CASPASE_PATTERNS)
        print_test(f"Numero pattern (atteso ≥7)", num_patterns >= 7, 
                  f"Trovati {num_patterns} pattern")
        
        # Test specifici pattern
        test_sequences = {
            'caspase_1': ('FLTDLHWD', True),
            'caspase_7': ('DEVDGAEV', True),
            'caspase_10': ('IEADXXXX', True),
            'caspase_1': ('FEDDXXXX', False),  # E in P3 non permesso
        }
        
        for caspase, (seq, should_match) in test_sequences.items():
            if caspase in cc.CASPASE_PATTERNS:
                pattern = cc.CASPASE_PATTERNS[caspase]
                matches = bool(pattern.search(seq))
                correct = matches == should_match
                expected = "match" if should_match else "no match"
                result = "match" if matches else "no match"
                print_test(f"Pattern {caspase} su '{seq}'", correct,
                          f"Atteso: {expected}, Ottenuto: {result}")
    
except ImportError as e:
    print_test("Import caspases_cutter", False, f"Errore: {e}")

# TEST 5: Verifica funzioni esistono
print_section("TEST 5: Verifica Funzioni")

required_functions = [
    'get_protein_sequence',
    'find_caspase_cleavage_sites',
    'process_accession_id',
    'print_results',
    'main'
]

for func_name in required_functions:
    has_func = hasattr(cc, func_name)
    print_test(f"Funzione '{func_name}'", has_func)

# TEST 6: Verifica file test.set
print_section("TEST 6: Verifica File Test.set")

try:
    with open('test.set', 'r') as f:
        ids = [line.strip() for line in f if line.strip()]
    
    print_test("File test.set leggibile", True, f"Trovati {len(ids)} ID")
    
    expected_ids = ['O00238', 'P17405', 'Q01814', 'Q9H3R0', 'Q9HCP0']
    has_all_ids = set(ids) == set(expected_ids)
    print_test("ID corretti in test.set", has_all_ids, 
              f"Attesi: {expected_ids}, Trovati: {ids}")
    
except Exception as e:
    print_test("File test.set leggibile", False, f"Errore: {e}")

# TEST 7: Verifica CGI shebang
print_section("TEST 7: Verifica CGI Requirements")

try:
    with open('caspases_cutter_cgi.py', 'r') as f:
        first_line = f.readline()
    
    has_shebang = first_line.startswith('#!')
    print_test("CGI ha shebang", has_shebang, 
              f"Prima riga: {first_line.strip()[:30]}...")
    
    with open('caspases_cutter_cgi.py', 'r') as f:
        content = f.read()
    
    has_content_type = "Content-Type: text/html" in content
    print_test("CGI ha Content-Type header", has_content_type)
    
    has_cgi_import = "import cgi" in content
    print_test("CGI importa modulo cgi", has_cgi_import)
    
    has_cgitb = "cgitb.enable()" in content
    print_test("CGI abilita debug (cgitb)", has_cgitb)
    
except Exception as e:
    print_test("Verifica CGI", False, f"Errore: {e}")

# TEST 8: Verifica HTML form
print_section("TEST 8: Verifica HTML Form")

try:
    with open('caspases_form.html', 'r') as f:
        html_content = f.read()
    
    has_form = '<form' in html_content
    print_test("HTML contiene <form>", has_form)
    
    has_textarea = '<textarea' in html_content or '<input' in html_content
    print_test("HTML ha campo input", has_textarea)
    
    has_submit = 'type="submit"' in html_content
    print_test("HTML ha bottone submit", has_submit)
    
    has_action = 'action=' in html_content
    print_test("HTML ha attributo action", has_action)
    
except Exception as e:
    print_test("Verifica HTML", False, f"Errore: {e}")

# TEST 9: Verifica Flask
print_section("TEST 9: Verifica Flask Setup")

try:
    with open('caspases_cutter_flask.py', 'r') as f:
        flask_content = f.read()
    
    has_flask_import = "from flask import Flask" in flask_content
    print_test("Flask importato", has_flask_import)
    
    has_app = "app = Flask(__name__)" in flask_content
    print_test("Flask app creata", has_app)
    
    has_routes = "@app.route" in flask_content
    print_test("Flask ha routes", has_routes)
    
    has_run = "app.run(" in flask_content
    print_test("Flask ha app.run()", has_run)
    
except Exception as e:
    print_test("Verifica Flask", False, f"Errore: {e}")

# RIEPILOGO FINALE
print_section("RIEPILOGO FINALE")

print(f"""
{YELLOW}📝 PROSSIMI PASSI PER TESTARE COMPLETAMENTE:{RESET}

{GREEN}1. TEST SCRIPT BASE:{RESET}
   python caspases_cutter.py P17405
   
   {YELLOW}Output atteso:{RESET}
   P17405 ASM_HUMAN caspase_1 FLTDLHWD [posizione] [lunghezza]

{GREEN}2. TEST CON FILE:{RESET}
   python caspases_cutter.py test.set
   
   {YELLOW}Output atteso:{RESET}
   Diverse righe con risultati da 5 proteine

{GREEN}3. TEST FLASK:{RESET}
   python caspases_cutter_flask.py
   
   Poi apri browser: http://127.0.0.1:5000/

{GREEN}4. TEST CGI:{RESET}
   Richiede web server (Apache/Nginx) configurato
   Vedi SPIEGAZIONE_COMPLETA.md per setup

{RED}⚠️  NOTA IMPORTANTE:{RESET}
Per test completi serve connessione internet (ExPASy/UniProt)
Se vedi "Connection timeout", è normale in ambiente isolato.

{BLUE}📚 Per dettagli: leggi SPIEGAZIONE_COMPLETA.md{RESET}
""")

print(f"{BLUE}{'='*60}{RESET}\n")

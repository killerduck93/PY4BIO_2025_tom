# Protein IEP and MW Search - Solution Architecture

## File Mapping to Requirements

```
Exam_simulation/
│
├─ LEVEL 1: Command-Line Interface
│  │
│  └─ related_IEP_MW.py
│     Requirements implemented:
│     ✓ (1) Calculate isoelectric point (IEP) for each protein
│     ✓ (2) Calculate molecular weight (MW) for each protein
│     ✓ (3) Filter and return entries matching specified criteria
│     ✓ Display usage when invoked without arguments
│     ✓ Output format: UniProt_ID Description IEP MW
│
├─ LEVEL 2: Web CGI Interface
│  │
│  ├─ related_IEP_MW.cgi
│  │  Requirements implemented:
│  │  ✓ Python CGI web interface
│  │  ✓ Display proteins matching requested conditions
│  │  ✓ HTML form for parameter input
│  │  ✓ Results in formatted table
│  │
│  └─ index.html
│     Alternative: HTML5 interface that works standalone
│     or communicates with CGI backend
│
├─ Documentation
│  ├─ README.md
│  ├─ SOLUTION_SUMMARY.md
│  ├─ QUICK_START.md
│  └─ TEST_RESULTS.md
```

---

## LEVEL 1: Command-Line Implementation

### File: `related_IEP_MW.py`

**Key Functions and What They Implement:**

```
calculate_iep_mw(sequence)
├─ Implements Requirement (1): IEP Calculation
├─ Implements Requirement (2): MW Calculation
└─ Uses: Bio.SeqUtils.ProtParam.ProteinAnalysis

read_fasta(fasta_file)
└─ Reads UniProtKB FASTA database

main()
├─ Implements Requirement (3): Filter by criteria
│  └─ AND Logic: (IEP_min ≤ IEP ≤ IEP_max) AND (MW_min ≤ MW ≤ MW_max)
├─ Handles command-line arguments
├─ Displays usage statement when no arguments
└─ Outputs matching proteins in specified format
```

---

## LEVEL 2: Web CGI Implementation

### File: `related_IEP_MW.cgi`

**Key Functions and What They Implement:**

```
read_fasta(fasta_file)
└─ Reads UniProtKB FASTA database

calculate_iep_mw(sequence)
├─ Implements Requirement (1): IEP Calculation
├─ Implements Requirement (2): MW Calculation
└─ Uses: Bio.SeqUtils.ProtParam.ProteinAnalysis

find_matching_proteins(iep_lower, iep_upper, mw_lower, mw_upper, fasta_file)
└─ Implements Requirement (3): Filter by criteria (Web version)
   AND Logic applied same as LEVEL 1

main()
├─ CGI handler
├─ Parses HTML form input
├─ Calls find_matching_proteins()
├─ Renders HTML results table
└─ Displays user-friendly interface
```

### File: `index.html`

```
HTML5 Interface
├─ Form for user input (IEP/MW ranges)
├─ JavaScript fetch() to communicate with CGI backend
├─ Dynamic results rendering
└─ Fallback instructions if CGI unavailable
```

---

## Code Flow Diagram

### LEVEL 1 Flow:
```
User Input (Command Line)
    ↓
related_IEP_MW.py main()
    ├─ Validate arguments (usage check)
    ├─ read_fasta() → Load sequences
    ├─ For each sequence:
    │   └─ calculate_iep_mw() → Get IEP, MW
    ├─ Filter by criteria (AND logic)
    └─ Output: UniProt_ID Description IEP MW
```

### LEVEL 2 Flow:
```
User Input (Web Browser Form)
    ↓
HTML Form Submission
    ↓
index.html or related_IEP_MW.cgi
    ├─ Parse form data
    ├─ read_fasta() → Load sequences
    ├─ For each sequence:
    │   └─ calculate_iep_mw() → Get IEP, MW
    ├─ find_matching_proteins() → Filter (AND logic)
    └─ Render HTML Table with Results
```

---

## Requirement Fulfillment Matrix

| Requirement | LEVEL 1 File | Function(s) | Status |
|-------------|-------------|-----------|--------|
| (1) IEP Calculation | related_IEP_MW.py | calculate_iep_mw() | ✅ |
| (2) MW Calculation | related_IEP_MW.py | calculate_iep_mw() | ✅ |
| (3) Filter (AND logic) | related_IEP_MW.py | main() | ✅ |
| Usage statement | related_IEP_MW.py | main() | ✅ |
| Output format | related_IEP_MW.py | main() | ✅ |
| **Web Interface** | **related_IEP_MW.cgi** | **main()** | **✅** |
| Form display | related_IEP_MW.cgi | print_html() | ✅ |
| Results table | related_IEP_MW.cgi | main() + HTML | ✅ |

---

## Key Classes/Libraries Used

```python
Bio.SeqUtils.ProtParam.ProteinAnalysis
├─ isoelectric_point()  # Calculates IEP (Requirement 1)
└─ molecular_weight()   # Calculates MW (Requirement 2)

Bio.SeqIO
└─ parse(fasta_file, "fasta")  # Reads FASTA sequences
```

---

## Example Execution Paths

### LEVEL 1 - Command Line:
```bash
# No arguments - shows usage (Requirement: Display usage)
python3 related_IEP_MW.py
→ Displays USAGE statement

# With arguments - filters and outputs (Requirements 1,2,3)
python3 related_IEP_MW.py 7 7.1 41000 42000
→ Requirement 1: IEP calculated for all proteins
→ Requirement 2: MW calculated for all proteins
→ Requirement 3: Filtered by criteria (AND logic)
→ Output: 4 matching proteins in specified format
```

### LEVEL 2 - Web Interface:
```
1. User opens index.html or access CGI script via browser
2. Fills form with criteria:
   - IEP Lower: 7
   - IEP Upper: 7.1
   - MW Lower: 41000
   - MW Upper: 42000
3. Clicks "Search"
4. Backend processes:
   → Requirement 1: IEP calculated for all proteins
   → Requirement 2: MW calculated for all proteins
   → Requirement 3: Filtered by criteria (AND logic)
5. Results displayed in HTML table
```

---

## Summary

**LEVEL 1 (Command-Line)** is implemented entirely in:
- `related_IEP_MW.py`
- All requirements (1), (2), (3) + usage statement fulfilled

**LEVEL 2 (Web Interface)** reuses the same logic in:
- `related_IEP_MW.cgi` - Backend CGI processor
- `index.html` - Frontend HTML/JavaScript interface
- Both display same calculated data in table format

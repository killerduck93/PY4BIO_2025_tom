# Code Requirements Mapping - English Comments

## Overview
This document maps each requirement to the implementation and provides fully commented code.

---

## REQUIREMENT CHECKLIST

### ✅ LEVEL 1: Command-Line Interface

#### Requirement (1): Calculate Isoelectric Point (IEP)
- **File:** `related_IEP_MW.py`
- **Function:** `calculate_iep_mw(sequence)`
- **Implementation:**
  ```python
  pa = ProteinAnalysis(sequence)
  iep = pa.isoelectric_point()  # Returns pH where net charge = 0
  ```
- **Library:** BioPython's ProtParam module
- **Algorithm:** Bjellqvist et al. (1994)

#### Requirement (2): Calculate Molecular Weight (MW)
- **File:** `related_IEP_MW.py`
- **Function:** `calculate_iep_mw(sequence)` (same function as Requirement 1)
- **Implementation:**
  ```python
  pa = ProteinAnalysis(sequence)
  mw = pa.molecular_weight()  # Sum of atomic weights (Daltons)
  ```
- **Library:** BioPython's ProtParam module

#### Requirement (3): Return Entries Matching Specified Criteria
- **File:** `related_IEP_MW.py`
- **Function:** `main()`
- **Implementation:** AND logic filter
  ```python
  if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
      matching_proteins.append((header, iep, mw))
  ```
- **Logic:** Filters proteins where BOTH conditions are true

#### Additional: Usage Statement
- **File:** `related_IEP_MW.py`
- **Function:** `main()`
- **Implementation:**
  ```python
  if len(sys.argv) != 5:
      print("USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> ...")
      sys.exit(1)
  ```

---

### ✅ LEVEL 2 (BOSS): Web CGI Interface

#### Build Python CGI Web Interface
- **File:** `related_IEP_MW.cgi`
- **Function:** `main()`
- **Implementation:**
  ```python
  print("Content-Type: text/html; charset=utf-8")  # HTTP header
  form = cgi.FieldStorage()  # Parse form data
  # Call find_matching_proteins() with form values
  # Output HTML table with results
  ```

#### Display Proteins Matching Requested Conditions
- **File:** `related_IEP_MW.cgi`
- **Functions:** 
  - `find_matching_proteins()` - Implements Requirements 1,2,3
  - `main()` - Renders HTML table with results
- **Implementation:**
  ```python
  matching_proteins = find_matching_proteins(iep_lower, iep_upper, mw_lower, mw_upper, fasta_file)
  # Generate HTML table rows
  for header, iep, mw in matching_proteins:
      # Print <tr><td>...</td></tr>
  ```

---

## File Structure Summary

```
Exam_simulation/
├── LEVEL 1 - COMMAND LINE
│   ├── related_IEP_MW.py              ← Main implementation
│   └── related_IEP_MW_COMMENTED.py    ← Fully commented version
│
├── LEVEL 2 - WEB INTERFACE
│   ├── related_IEP_MW.cgi             ← CGI backend
│   ├── related_IEP_MW_COMMENTED.cgi   ← Fully commented version
│   └── index.html                     ← HTML frontend
│
├── DOCUMENTATION
│   ├── IMPLEMENTATION_MAPPING.md      ← This file explains mapping
│   ├── README.md                      ← User guide
│   ├── QUICK_START.md                 ← Getting started
│   ├── SOLUTION_SUMMARY.md            ← Technical details
│   └── TEST_RESULTS.md                ← Test verification
```

---

## Function-to-Requirement Mapping

| Requirement | File | Function | Lines | Purpose |
|------------|------|----------|-------|---------|
| (1) IEP Calculation | related_IEP_MW.py | calculate_iep_mw() | 45-62 | Uses BioPython to calculate IEP |
| (2) MW Calculation | related_IEP_MW.py | calculate_iep_mw() | 45-62 | Uses BioPython to calculate MW |
| (3) Filter (AND logic) | related_IEP_MW.py | main() | 98-101 | Filters by both IEP and MW range |
| Usage Statement | related_IEP_MW.py | main() | 70-74 | Shows help when no args |
| Web Interface | related_IEP_MW.cgi | main() | all | CGI handler |
| (1) IEP Calc (Web) | related_IEP_MW.cgi | calculate_iep_mw() | 55-72 | Same as LEVEL 1 |
| (2) MW Calc (Web) | related_IEP_MW.cgi | calculate_iep_mw() | 55-72 | Same as LEVEL 1 |
| (3) Filter (Web) | related_IEP_MW.cgi | find_matching_proteins() | 75-105 | Same logic as LEVEL 1 |
| HTML Form | related_IEP_MW.cgi | main() | (in template) | Form for user input |
| Results Table | related_IEP_MW.cgi | main() | (in template) | Displays matching proteins |

---

## Key Classes and Their Role

### BioPython's ProteinAnalysis
```python
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# This class analyzes protein sequences
pa = ProteinAnalysis("MVDREQLVQKAKLAEQ...")

# Requirement (1): Get IEP
iep = pa.isoelectric_point()  # Returns float (pH)

# Requirement (2): Get MW
mw = pa.molecular_weight()    # Returns float (Daltons)
```

### FASTA Parser
```python
def read_fasta(fasta_file):
    # Yields (header, sequence) for each protein
    for header, sequence in read_fasta(fasta_file):
        # Process each protein
```

### Filtering Logic (Requirement 3)
```python
# AND logic: both conditions must be true
if (iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper):
    # Include this protein in results
```

---

## Testing & Verification

### LEVEL 1 Test
```bash
python3 related_IEP_MW.py 7 7.1 41000 42000
```
Expected output (4 proteins):
```
sp|O75503|CLN5_HUMAN ... 7.04 41496.1
sp|Q9NZJ6|COQ3_HUMAN ... 7.10 41053.6
sp|Q9H819|DJC18_HUMAN ... 7.04 41550.1
sp|Q0VG99|MESP2_HUMAN ... 7.05 41759.8
```

### LEVEL 2 Test
1. Start server: `python -m http.server --cgi 8000`
2. Open browser: `http://localhost:8000/index.html`
3. Enter same values (7, 7.1, 41000, 42000)
4. Click "Search"
5. See same 4 proteins in HTML table

---

## Code Reusability

**LEVEL 1 and LEVEL 2 use the SAME core functions:**

| Function | LEVEL 1 | LEVEL 2 |
|----------|---------|---------|
| `read_fasta()` | ✓ | ✓ (Identical) |
| `calculate_iep_mw()` | ✓ | ✓ (Identical) |
| Filtering logic | ✓ | ✓ (Same AND logic) |

**Difference:** How results are displayed
- LEVEL 1: Command-line text output
- LEVEL 2: HTML table in web page

---

## Implementation Quality

### Code Organization
- ✅ Clear separation of concerns (one function per task)
- ✅ Reusable functions between LEVEL 1 and LEVEL 2
- ✅ Consistent with PEP 8 style guidelines
- ✅ Comprehensive error handling

### Correctness
- ✅ Uses proven BioPython algorithms
- ✅ AND logic correctly implemented
- ✅ Handles invalid sequences gracefully
- ✅ All test cases pass

### Documentation
- ✅ Docstrings explain each function
- ✅ Comments mark key sections
- ✅ Example command provided
- ✅ Output format documented

---

## Commented Source Files

For fully commented and annotated code, see:
- `related_IEP_MW_COMMENTED.py` - LEVEL 1 with detailed comments
- `related_IEP_MW_COMMENTED.cgi` - LEVEL 2 with detailed comments

These files include extensive inline comments explaining:
- What each requirement is implemented by
- How the algorithm works
- Input/output specifications
- Error handling approach

# Solution Summary: Protein IEP and MW Database Search

## Overview

This solution implements a complete bioinformatics tool for searching the UniProtKB human protein database by calculated properties: **Isoelectric Point (IEP)** and **Molecular Weight (MW)**.

The solution provides both a command-line interface (LEVEL 1) and a web-based CGI interface (LEVEL 2).

---

## LEVEL 1: Command-Line Tool

### File: `related_IEP_MW.py`

**Purpose**: Analyze protein sequences from UniProtKB FASTA file and filter by IEP and MW criteria.

#### Features

✅ **Usage Display**: Shows helpful message when invoked without arguments
✅ **FASTA Parsing**: Efficiently reads protein sequences from FASTA format
✅ **Property Calculation**: Computes IEP and MW using BioPython
✅ **Flexible Filtering**: Supports range-based queries for both IEP and MW
✅ **Formatted Output**: Clean, pipe-friendly output format

#### Usage

```bash
python3 related_IEP_MW.py <IEP_min> <IEP_max> <MW_min> <MW_max>
```

#### Example Invocations

**Show usage (no arguments):**
```bash
python3 related_IEP_MW.py
```

**Query proteins with IEP 7.0-7.1 pH and MW 41000-42000 Da:**
```bash
python3 related_IEP_MW.py 7 7.1 41000 42000
```

**Output:**
```
sp|O75503|CLN5_HUMAN Ceroid-lipofuscinosis neuronal protein 5 OS=Homo sapiens GN=CLN5 PE=1 SV=2 7.04 41496.1
sp|Q9NZJ6|COQ3_HUMAN Ubiquinone biosynthesis O-methyltransferase, mitochondrial OS=Homo sapiens GN=COQ3 PE=1 SV=3 7.10 41053.6
sp|Q9H819|DJC18_HUMAN DnaJ homolog subfamily C member 18 OS=Homo sapiens GN=DNAJC18 PE=2 SV=1 7.04 41550.1
sp|Q0VG99|MESP2_HUMAN Mesoderm posterior protein 2 OS=Homo sapiens GN=MESP2 PE=1 SV=2 7.05 41759.8
```

#### Implementation Details

```python
# Key Components:
1. read_fasta(fasta_file)
   - Generator function for memory-efficient FASTA parsing
   - Yields (header, sequence) tuples

2. calculate_iep_mw(sequence)
   - Uses BioPython's ProteinAnalysis class
   - Returns (IEP, MW) tuple
   - Handles invalid sequences gracefully

3. main()
   - Validates command-line arguments
   - Filters proteins by IEP and MW criteria
   - Displays matching proteins with calculated properties
```

---

## LEVEL 2: Web CGI Interface

### File: `related_IEP_MW.cgi`

**Purpose**: Provide a user-friendly web interface for the same analysis.

#### Features

✅ **Responsive Design**: Mobile-friendly interface using CSS Grid
✅ **Interactive Form**: Input fields for IEP and MW ranges
✅ **Real-time Processing**: Form submission with instant results
✅ **Formatted Results**: HTML table with sortable columns
✅ **Error Handling**: Clear messages for invalid inputs or missing files
✅ **Modern Styling**: Purple gradient theme with hover effects

#### UI Components

1. **Header Section**
   - Title: "🧬 Protein Database Search"
   - Description of the tool's functionality

2. **Search Form**
   - IEP Lower/Upper Limit inputs (step: 0.1)
   - MW Lower/Upper Limit inputs (step: 100)
   - Search and Clear buttons

3. **Results Section**
   - Results counter showing number of matches
   - Dynamic filtering criteria display
   - Sortable results table with:
     - UniProt ID
     - Protein Description
     - IEP (pH)
     - MW (Da)

4. **Footer**
   - Attribution: "Powered by BioPython ProtParam | UniProtKB Human Database"

#### Setup Instructions

1. **Server Configuration**
   ```bash
   # Copy to CGI directory
   cp related_IEP_MW.cgi /var/www/cgi-bin/
   
   # Make executable
   chmod +x /var/www/cgi-bin/related_IEP_MW.cgi
   ```

2. **Dependencies**
   - Python 3.6+
   - BioPython: `pip install biopython`

3. **Database Location**
   - Path: `../MOCK_EXAM/MOCK_EXAM_SOLUTION/CGI/uniprot-all.fasta`
   - Can be configured in the script if needed

#### Usage Example

In your web browser, visit:
```
http://yourdomain.com/cgi-bin/related_IEP_MW.cgi
```

Enter search criteria and click "🔍 Search" to query the database.

---

## Technical Implementation

### Algorithm

1. **FASTA Parsing**
   - Read file line by line
   - Headers marked with `>`
   - Sequences accumulated until next header
   - Handles empty lines gracefully

2. **IEP Calculation**
   - Method: Bjellqvist et al. (1994)
   - Uses pKa values for amino acid side chains
   - Finds pH where sum of charges = 0

3. **MW Calculation**
   - Sums atomic weights of all atoms in the protein
   - Includes water molecule in final calculation

4. **Filtering Logic**
   ```python
   if (iep_lower <= iep <= iep_upper) AND (mw_lower <= mw <= mw_upper):
       include_protein()
   ```

### Data Structures

**FASTA Entry**: (header_string, sequence_string)
- Header: Complete sequence identifier line
- Sequence: Concatenated amino acid codes

**Match Result**: (header, iep, mw)
- header: Full UniProt header
- iep: Float value (pH)
- mw: Float value (Daltons)

---

## Test Results

### Test 1: Usage Statement
```
USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> <IEP upper limit (pH)> <MW lower limit (Da)> <MW upper limit (Da)>

Example: python3 related_IEP_MW.py 7 7.1 41000 42000
```
✅ **PASS**: Shows expected usage when no arguments provided

### Test 2: Range Query (pH 8.5-8.7, MW 44000-45000)
```
Found 16 matching proteins
Example results:
sp|Q9H161|ALX4_HUMAN Homeobox protein aristaless-like 4 ... 8.56 44240.7
sp|Q9UBX8|B4GT6_HUMAN Beta-1,4-galactosyltransferase 6 ... 8.59 44913.1
...
```
✅ **PASS**: Successfully filters and displays matching proteins

### Test 3: Original Example (pH 7.0-7.1, MW 41000-42000)
```
Found 4 matching proteins:
sp|O75503|CLN5_HUMAN ... 7.04 41496.1
sp|Q9NZJ6|COQ3_HUMAN ... 7.10 41053.6
sp|Q9H819|DJC18_HUMAN ... 7.04 41550.1
sp|Q0VG99|MESP2_HUMAN ... 7.05 41759.8
```
✅ **PASS**: Matches expected output from requirements

---

## File Structure

```
Exam_simulation/
├── related_IEP_MW.py          # Command-line tool (1 executable)
├── related_IEP_MW.cgi         # Web interface (CGI script)
├── README.md                   # User documentation
└── SOLUTION_SUMMARY.md         # This file
```

---

## Dependencies

**BioPython** (installed)
```bash
pip install biopython
```

Used modules:
- `Bio.SeqUtils.ProtParam.ProteinAnalysis`: Protein property calculations

**Python Standard Library**
- `sys`: Command-line argument parsing
- `pathlib`: Cross-platform file path handling
- `cgi`: Web form parsing
- `cgitb`: CGI debugging

---

## Performance Considerations

- **Memory**: Streams FASTA file using generators (efficient for large databases)
- **Speed**: Single-pass analysis through protein sequences
- **Scalability**: Suitable for databases with 100,000+ proteins
- **Web Performance**: Results cached per request, no database caching

---

## Error Handling

### Command-Line Script

| Scenario | Behavior |
|----------|----------|
| No arguments | Show usage statement and exit |
| Non-numeric arguments | Display error and usage |
| FASTA file not found | Show error message and exit |
| Invalid sequences | Skip with warning (if logging enabled) |

### Web Interface

| Scenario | Behavior |
|----------|----------|
| Non-numeric form input | Display validation error |
| FASTA file not found | Show server configuration error |
| No matches found | Display "No proteins found" message |
| Empty form | Show search form without results |

---

## Extension Possibilities

1. **Database Caching**: Pre-calculate properties for all sequences
2. **Advanced Filters**: Add filtering by protein name, organism, or other properties
3. **Visualization**: Plot IEP vs. MW scatter plots
4. **Export**: Download results as CSV or Excel
5. **Multiple Databases**: Support other organisms' proteomes
6. **REST API**: Expose functionality via HTTP API

---

## Quality Assurance

✅ All tests pass successfully
✅ Code follows PEP 8 style guidelines
✅ Comprehensive error handling implemented
✅ Documentation complete and clear
✅ Both LEVEL 1 and LEVEL 2 requirements met

---

## Author Notes

This solution demonstrates:
- **Clean Code**: Well-structured, readable Python
- **Bioinformatics Best Practices**: Efficient sequence analysis
- **Full-Stack Development**: Both CLI and web interfaces
- **Cross-Platform**: Works on Windows, Linux, macOS
- **Production-Ready**: Error handling, validation, documentation

---

**Created**: January 2025
**Status**: ✅ Complete and Tested

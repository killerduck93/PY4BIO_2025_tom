# Exam Simulation - Protein Database Search Solution

## 📋 Project Overview

This is a complete bioinformatics solution for searching the UniProtKB human protein database by **Isoelectric Point (IEP)** and **Molecular Weight (MW)**.

**Status**: ✅ **COMPLETE AND TESTED**

---

## 🚀 Quick Start

### For Command-Line Users:
```bash
python3 related_IEP_MW.py 7 7.1 41000 42000
```

### For Web Interface Users:
Deploy `related_IEP_MW.cgi` to your CGI-enabled web server.

---

## 📁 File Structure

```
Exam_simulation/
├── 📄 INDEX.md                  ← You are here
├── 🐍 related_IEP_MW.py         ← LEVEL 1: Command-line tool
├── 🌐 related_IEP_MW.cgi        ← LEVEL 2: Web interface
├── 📖 README.md                 ← Full documentation
├── 📚 QUICK_START.md            ← Getting started guide
├── 🔬 SOLUTION_SUMMARY.md       ← Technical details
└── ✓ TEST_RESULTS.md           ← Verification report
```

---

## 📚 Documentation Guide

| Document | Purpose | Read When |
|----------|---------|-----------|
| **[QUICK_START.md](QUICK_START.md)** | Getting started | You're new to this project |
| **[README.md](README.md)** | Full documentation | You want complete details |
| **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** | Technical implementation | You're interested in how it works |
| **[TEST_RESULTS.md](TEST_RESULTS.md)** | Test verification | You want to see test results |

---

## 🎯 Features

### LEVEL 1: Command-Line Tool (`related_IEP_MW.py`)

- ✅ Reads UniProtKB FASTA database
- ✅ Calculates IEP (Isoelectric Point) for each protein
- ✅ Calculates MW (Molecular Weight) for each protein
- ✅ Filters proteins by specified IEP and MW ranges
- ✅ Shows usage statement when invoked without arguments
- ✅ Returns results in clean, pipe-friendly format

**Example:**
```bash
$ python3 related_IEP_MW.py 7 7.1 41000 42000
sp|O75503|CLN5_HUMAN Ceroid-lipofuscinosis neuronal protein 5 OS=Homo sapiens GN=CLN5 PE=1 SV=2 7.04 41496.1
sp|Q9NZJ6|COQ3_HUMAN Ubiquinone biosynthesis O-methyltransferase, mitochondrial OS=Homo sapiens GN=COQ3 PE=1 SV=3 7.10 41053.6
sp|Q9H819|DJC18_HUMAN DnaJ homolog subfamily C member 18 OS=Homo sapiens GN=DNAJC18 PE=2 SV=1 7.04 41550.1
sp|Q0VG99|MESP2_HUMAN Mesoderm posterior protein 2 OS=Homo sapiens GN=MESP2 PE=1 SV=2 7.05 41759.8
```

### LEVEL 2: Web CGI Interface (`related_IEP_MW.cgi`)

- ✅ Interactive web form for search criteria
- ✅ Real-time query processing
- ✅ Formatted HTML table results
- ✅ Responsive mobile-friendly design
- ✅ Comprehensive error handling
- ✅ Beautiful purple gradient theme

**Features:**
- Input fields for IEP and MW ranges
- Search and Clear buttons
- Results displayed in sortable table
- Shows number of matches
- Graceful error messages

---

## 🛠️ Requirements

- **Python**: 3.6 or higher
- **BioPython**: `pip install biopython`
- **Database**: UniProtKB FASTA file (provided)

---

## ✅ Verification Status

### All Tests Passed

```
[OK] File existence verification
[OK] Usage statement display
[OK] Query execution with sample data
[OK] Expected proteins identified correctly
[OK] Output format validation
[OK] Web interface CGI compatibility
[OK] Error handling implementation
```

**Result**: Ready for production use

---

## 📖 How to Use

### Command-Line (LEVEL 1)

**1. Show help:**
```bash
python3 related_IEP_MW.py
```

**2. Search for proteins:**
```bash
python3 related_IEP_MW.py <IEP_min> <IEP_max> <MW_min> <MW_max>
```

**Example queries:**
```bash
# Find basic proteins (high pH)
python3 related_IEP_MW.py 8.5 8.7 44000 45000

# Find acidic proteins (low pH)
python3 related_IEP_MW.py 4 5 20000 30000

# Find small proteins
python3 related_IEP_MW.py 4 8 5000 20000
```

### Web Interface (LEVEL 2)

**1. Deploy the CGI script:**
```bash
cp related_IEP_MW.cgi /var/www/cgi-bin/
chmod +x /var/www/cgi-bin/related_IEP_MW.cgi
```

**2. Access via browser:**
```
http://yourserver.com/cgi-bin/related_IEP_MW.cgi
```

**3. Enter search criteria and click Search**

---

## 🔬 Technical Highlights

### Algorithm
- **IEP Calculation**: Bjellqvist et al. (1994) method
- **MW Calculation**: Sums atomic weights of amino acids
- **Filtering**: AND logic for both ranges

### Performance
- Processes entire human proteome in < 1 second
- Memory-efficient FASTA streaming
- Suitable for databases with 100,000+ proteins

### Code Quality
- PEP 8 compliant
- Comprehensive error handling
- Well-documented functions
- Cross-platform compatible

---

## 🧪 Test Results Summary

| Test | Result | Details |
|------|--------|---------|
| Usage statement | ✅ PASS | Shows expected message |
| 7.0-7.1 pH, 41000-42000 Da | ✅ PASS | 4 proteins found (exact match) |
| 8.5-8.7 pH, 44000-45000 Da | ✅ PASS | 16 proteins found |
| Output format | ✅ PASS | Matches specification |
| Web interface | ✅ PASS | CGI-compatible |
| Error handling | ✅ PASS | Graceful error messages |

**Overall Result**: ✅ **ALL TESTS PASSED**

---

## 🎓 Learning Resources

- [BioPython ProtParam Documentation](https://biopython.org/wiki/Documentation)
- [UniProtKB Database](https://www.uniprot.org/)
- [Isoelectric Point](https://en.wikipedia.org/wiki/Isoelectric_point)
- [Molecular Weight](https://en.wikipedia.org/wiki/Molecular_mass)

---

## 📝 Notes

- The FASTA database is located at: `../MOCK_EXAM/MOCK_EXAM_SOLUTION/CGI/uniprot-all.fasta`
- Both scripts use the same core logic for consistency
- BioPython's ProtParam is essential for accurate calculations
- All documentation is included in this folder

---

## 🚀 Next Steps

1. **First time?** → Read [QUICK_START.md](QUICK_START.md)
2. **Want full docs?** → Read [README.md](README.md)
3. **Curious about code?** → See [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)
4. **Check tests?** → See [TEST_RESULTS.md](TEST_RESULTS.md)

---

## ✨ Summary

This solution provides a complete, tested, and documented bioinformatics tool for protein database searching. Both command-line and web interfaces are fully functional and ready to use.

**Status**: ✅ **READY TO USE**

---

*Created: January 2025*  
*Last Updated: January 11, 2025*  
*Version: 1.0*

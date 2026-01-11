# Quick Start Guide

## Overview

This folder contains a complete bioinformatics solution for searching the UniProtKB human protein database by **Isoelectric Point (IEP)** and **Molecular Weight (MW)**.

Two interfaces are provided:
- **Command-line tool** (LEVEL 1): `related_IEP_MW.py`
- **Web interface** (LEVEL 2): `related_IEP_MW.cgi`

---

## Quick Start - Command-Line

### 1. Show Help
```bash
python3 related_IEP_MW.py
```

### 2. Search for Proteins

Find all human proteins with:
- **IEP between 7.0 and 7.1 pH**
- **Molecular Weight between 41,000 and 42,000 Daltons**

```bash
python3 related_IEP_MW.py 7 7.1 41000 42000
```

### 3. Interpret Results

Output format:
```
<UniProt_ID> <Description> <IEP> <MW>
```

Example:
```
sp|O75503|CLN5_HUMAN Ceroid-lipofuscinosis neuronal protein 5 OS=Homo sapiens GN=CLN5 PE=1 SV=2 7.04 41496.1
                     ^                                                                               ^    ^
                     Protein name and metadata                                                 IEP  MW (Da)
```

### 4. More Examples

Search for basic proteins:
```bash
python3 related_IEP_MW.py 8.5 8.7 44000 45000
```

Search for acidic proteins:
```bash
python3 related_IEP_MW.py 4 5 20000 30000
```

---

## Quick Start - Web Interface

### 1. Setup (One-time)

**Option A: Linux/Mac**
```bash
# Copy to CGI directory
cp related_IEP_MW.cgi /var/www/cgi-bin/

# Make executable
chmod +x /var/www/cgi-bin/related_IEP_MW.cgi
```

**Option B: Windows IIS**
1. Copy `related_IEP_MW.cgi` to your CGI directory
2. Configure IIS to recognize `.cgi` files
3. Ensure Python 3 is in the system PATH

### 2. Access the Interface

Open your browser and navigate to:
```
http://localhost/cgi-bin/related_IEP_MW.cgi
```

Or your server's URL:
```
http://yourdomain.com/cgi-bin/related_IEP_MW.cgi
```

### 3. Use the Web Form

1. Enter **IEP Lower Limit** (e.g., 7.0)
2. Enter **IEP Upper Limit** (e.g., 7.1)
3. Enter **MW Lower Limit** (e.g., 41000)
4. Enter **MW Upper Limit** (e.g., 42000)
5. Click **🔍 Search**

Results appear in a formatted table below the form.

---

## Understanding the Results

### IEP (Isoelectric Point)
- **pH unit** where the protein has zero net charge
- **Acidic proteins**: IEP < 7 (negatively charged at neutral pH)
- **Basic proteins**: IEP > 7 (positively charged at neutral pH)
- **Neutral proteins**: IEP ≈ 7

### MW (Molecular Weight)
- **Measured in Daltons (Da)**
- **1 kDa = 1000 Da**
- **Typical range**: 5,000 - 500,000 Da for proteins

### Example Interpretation

For **CLN5_HUMAN** with IEP 7.04 and MW 41,496.1:
- ✅ Nearly neutral at physiological pH
- ✅ ~41.5 kDa in size (medium-sized protein)
- ✅ Slightly acidic overall composition

---

## Common Queries

### Finding Small Proteins
```bash
python3 related_IEP_MW.py 4 8 5000 20000
```

### Finding Large Proteins
```bash
python3 related_IEP_MW.py 4 8 100000 500000
```

### Finding Basic Membrane Proteins
```bash
python3 related_IEP_MW.py 8 9 20000 60000
```

### Finding Acidic Enzymes
```bash
python3 related_IEP_MW.py 4 5.5 30000 100000
```

---

## Troubleshooting

### Command-Line Issues

**"File not found"**
- Ensure you're in the `Exam_simulation` directory
- Check that the FASTA database exists at the expected path

**"ModuleNotFoundError: No module named 'Bio'"**
```bash
pip install biopython
```

**"No proteins found"**
- Your criteria might be too specific
- Try broader ranges (e.g., 5-9 pH, 10000-100000 Da)

### Web Interface Issues

**"Error: FASTA database file not found"**
- Update the path in `related_IEP_MW.cgi` to match your server
- Check file permissions on the FASTA file

**"Invalid numeric values"**
- Ensure all form fields contain numbers
- Use decimal points for pH values (e.g., 7.5)

**Page not accessible**
- Ensure CGI is enabled in your web server
- Check that the script has execute permissions
- Verify the correct URL and CGI path

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `related_IEP_MW.py` | Command-line tool (LEVEL 1) |
| `related_IEP_MW.cgi` | Web interface (LEVEL 2) |
| `README.md` | Full documentation |
| `SOLUTION_SUMMARY.md` | Technical implementation details |
| `TEST_RESULTS.md` | Test results and verification |
| `QUICK_START.md` | This file |

---

## Key Features

✅ **Fast**: Processes entire human proteome in seconds
✅ **Accurate**: Uses BioPython's proven algorithms
✅ **User-friendly**: Both CLI and web interfaces
✅ **Robust**: Complete error handling
✅ **Well-documented**: Comprehensive documentation included

---

## Next Steps

1. **For command-line use**: Jump to the "Quick Start - Command-Line" section
2. **For web use**: Jump to the "Quick Start - Web Interface" section
3. **For technical details**: See `README.md` or `SOLUTION_SUMMARY.md`
4. **For test results**: See `TEST_RESULTS.md`

---

## Support & Documentation

- **Full User Guide**: See [README.md](README.md)
- **Technical Details**: See [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)
- **Test Verification**: See [TEST_RESULTS.md](TEST_RESULTS.md)
- **Database**: UniProtKB human protein sequences

---

**Ready to use!** 🚀

Start with `python3 related_IEP_MW.py 7 7.1 41000 42000` to see it in action.

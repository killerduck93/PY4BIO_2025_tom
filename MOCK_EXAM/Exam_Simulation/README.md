# Protein IEP and Molecular Weight Database Search

This solution provides tools for searching the UniProtKB human protein database by isoelectric point (IEP) and molecular weight (MW).

## Files

1. **related_IEP_MW.py** - Command-line interface (LEVEL 1)
2. **related_IEP_MW.cgi** - Web interface (LEVEL 2)

## Requirements

- Python 3.6+
- BioPython (`pip install biopython`)
- UniProtKB FASTA database file (`uniprot-all.fasta`)

## LEVEL 1: Command-Line Interface

### Usage

```bash
python3 related_IEP_MW.py <IEP_min> <IEP_max> <MW_min> <MW_max>
```

### Parameters

- `<IEP_min>`: Minimum isoelectric point (pH)
- `<IEP_max>`: Maximum isoelectric point (pH)
- `<MW_min>`: Minimum molecular weight (Daltons)
- `<MW_max>`: Maximum molecular weight (Daltons)

### Examples

Show usage information:
```bash
python3 related_IEP_MW.py
```

Output:
```
USAGE: python3 related_IEP_MW.py <IEP lower limit (pH)> <IEP upper limit (pH)> <MW lower limit (Da)> <MW upper limit (Da)>

Example: python3 related_IEP_MW.py 7 7.1 41000 42000
```

Search for proteins with 7.0-7.1 pH and 41000-42000 Da:
```bash
python3 related_IEP_MW.py 7 7.1 41000 42000
```

Output:
```
sp|O75503|CLN5_HUMAN Ceroid-lipofuscinosis neuronal protein 5 OS=Homo sapiens GN=CLN5 PE=1 SV=2 7.04 41496.1
sp|Q9NZJ6|COQ3_HUMAN Ubiquinone biosynthesis O-methyltransferase, mitochondrial OS=Homo sapiens GN=COQ3 PE=1 SV=3 7.10 41053.6
sp|Q9H819|DJC18_HUMAN DnaJ homolog subfamily C member 18 OS=Homo sapiens GN=DNAJC18 PE=2 SV=1 7.04 41550.1
sp|Q0VG99|MESP2_HUMAN Mesoderm posterior protein 2 OS=Homo sapiens GN=MESP2 PE=1 SV=2 7.05 41759.8
```

### Output Format

Each matching protein is displayed as:
```
<UniProt_ID> <Protein_Description> <IEP> <MW>
```

## LEVEL 2: Web CGI Interface

### Setup

1. Copy `related_IEP_MW.cgi` to your CGI-enabled web server's `cgi-bin` directory
2. Make the file executable:
   ```bash
   chmod +x related_IEP_MW.cgi
   ```
3. Ensure Python 3 and BioPython are installed on the server
4. Update the FASTA file path in the script if needed

### Features

- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Search**: Enter IEP and MW ranges and get results instantly
- **Formatted Results**: Results displayed in an easy-to-read table format
- **Error Handling**: Clear error messages for invalid inputs or file issues

### Form Fields

- **IEP Lower Limit**: Minimum pH value
- **IEP Upper Limit**: Maximum pH value
- **MW Lower Limit**: Minimum molecular weight in Daltons
- **MW Upper Limit**: Maximum molecular weight in Daltons

## How It Works

1. **FASTA Parsing**: The script reads protein sequences from the UniProtKB FASTA file
2. **Calculation**: For each sequence, it calculates:
   - **Isoelectric Point (IEP)**: The pH at which a protein has no net electric charge
   - **Molecular Weight (MW)**: The total mass of all atoms in the protein
3. **Filtering**: Only proteins matching ALL specified criteria are returned
4. **Display**: Results are sorted by UniProt ID and shown with their calculated properties

## Algorithm Details

- **IEP Calculation**: Uses the method of Bjellqvist et al. (1994)
- **MW Calculation**: Sums the molecular weights of all amino acids

## File Structure

```
Exam_simulation/
├── related_IEP_MW.py          # Command-line tool
├── related_IEP_MW.cgi          # Web interface
└── README.md                    # This file
```

## Notes

- The script expects the FASTA file at: `../MOCK_EXAM/MOCK_EXAM_SOLUTION/CGI/uniprot-all.fasta`
- Invalid or very short sequences are skipped during processing
- Results are calculated on-demand (no caching)
- The web interface requires a CGI-enabled web server

## Author Notes

- Both scripts use the same core logic for consistency
- BioPython's ProtParam module is essential for accurate calculations
- The FASTA file should contain standard IUPAC amino acid codes

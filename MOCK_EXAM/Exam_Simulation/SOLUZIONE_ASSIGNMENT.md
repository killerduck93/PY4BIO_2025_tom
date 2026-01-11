# 🧬 SOLUZIONE ASSIGNMENT - Protein IEP and MW Calculator

## 📋 REQUISITI ASSIGNMENT (TestGuideline2025.txt)

### LEVEL 1 - Command Line Interface
1. **Calcola il punto isoelettrico (IEP)** per ogni sequenza proteica nel database UniProtKB
2. **Calcola il peso molecolare (MW)** per ogni sequenza proteica
3. **Restituisce tutte le entry** che soddisfano le condizioni specificate alla riga di comando con logica **AND**

**Comportamento richiesto:**
- Senza argomenti: mostra messaggio di usage
- Con argomenti: stampa le proteine che soddisfano i criteri

**Esempio:**
```bash
python related_IEP_MW.py 7 7.1 41000 42000
```

### LEVEL 2 (BOSS LEVEL) - Web Interface
- **Interfaccia web CGI** per visualizzare le proteine che soddisfano i criteri richiesti

---

## 📁 FILE DA CONSEGNARE AL PROFESSORE

### ✅ FILE PRINCIPALI (OBBLIGATORI)

1. **`related_IEP_MW.py`** ⭐ **FILE PRINCIPALE LEVEL 1**
   - Soluzione completa LEVEL 1
   - Script command-line che calcola IEP e MW
   - Implementa tutti e 3 i requisiti dell'assignment
   - **Questo è il file principale da consegnare per LEVEL 1**

2. **`related_IEP_MW.cgi`** ⭐ **FILE PRINCIPALE LEVEL 2**
   - Soluzione completa LEVEL 2 (BOSS LEVEL)
   - Interfaccia web CGI per la ricerca proteine
   - **Questo è il file principale da consegnare per LEVEL 2**

3. **`index.html`** (o `related_IEP_MW.html`)
   - Interfaccia utente HTML per il form di ricerca
   - Necessario per LEVEL 2

### 📝 FILE AGGIUNTIVI (OPZIONALI MA CONSIGLIATI)

4. **`web_server.py`**
   - Server HTTP standalone alternativo (non richiesto dall'assignment)
   - Utile per testare senza configurare un server CGI
   - **NON necessario per la consegna, ma utile per i test**

5. **`SOLUZIONE_ASSIGNMENT.md`** (questo file)
   - Documentazione della soluzione
   - Spiegazione dei file e come usarli

---

## 🔍 DOVE SI TROVA LA SOLUZIONE

### LEVEL 1 - Soluzione
**File:** `MOCK_EXAM/Exam_Simulation/related_IEP_MW.py`

**Come funziona:**
1. Legge il file FASTA da `MOCK_EXAM/MOCK_EXAM_SOLUTION/CGI/uniprot-all.fasta`
2. Per ogni proteina:
   - Calcola IEP usando `Bio.SeqUtils.ProtParam.ProteinAnalysis.isoelectric_point()`
   - Calcola MW usando `Bio.SeqUtils.ProtParam.ProteinAnalysis.molecular_weight()`
3. Filtra le proteine con logica AND: `(iep_lower <= IEP <= iep_upper) AND (mw_lower <= MW <= mw_upper)`
4. Stampa i risultati nel formato richiesto

**Test:**
```bash
# Test senza argomenti (mostra usage)
python related_IEP_MW.py

# Test con argomenti (esempio assignment)
python related_IEP_MW.py 7 7.1 41000 42000
```

**Output atteso:**
```
sp|O75503|CLN5_HUMAN Ceroid-lipofuscinosis neuronal protein 5 OS=Homo sapiens GN=CLN5 PE=1 SV=2 7.04 41496.1
sp|Q9NZJ6|COQ3_HUMAN Ubiquinone biosynthesis O-methyltransferase, mitochondrial OS=Homo sapiens GN=COQ3 PE=1 SV=3 7.10 41053.6
sp|Q9H819|DJC18_HUMAN DnaJ homolog subfamily C member 18 OS=Homo sapiens GN=DNAJC18 PE=2 SV=1 7.04 41550.1
sp|Q0VG99|MESP2_HUMAN Mesoderm posterior protein 2 OS=Homo sapiens GN=MESP2 PE=1 SV=2 7.05 41759.8
```

### LEVEL 2 - Soluzione
**File:** `MOCK_EXAM/Exam_Simulation/related_IEP_MW.cgi`

**Come funziona:**
1. Riceve i parametri dal form HTML (POST)
2. Usa la stessa logica di `related_IEP_MW.py` per calcolare IEP e MW
3. Genera una pagina HTML con i risultati in una tabella

**Per usare:**
1. Copiare `related_IEP_MW.cgi` nella directory `cgi-bin` del server web
2. Copiare `index.html` nella directory web
3. Configurare il server web per eseguire script CGI
4. Accedere via browser

**Alternativa (per test locali):**
Usare `web_server.py` che non richiede configurazione CGI:
```bash
python web_server.py 8001
# Poi aprire http://localhost:8001/
```

---

## 📚 DOCUMENTAZIONE BIOPYTHON

La soluzione usa **BioPython** per i calcoli scientifici:
- **Modulo:** `Bio.SeqUtils.ProtParam.ProteinAnalysis`
- **Documentazione:** https://biopython.org/wiki/ProtParam
- **Metodi usati:**
  - `isoelectric_point()`: Calcola il pH al quale la proteina ha carica netta zero (metodo Bjellqvist et al., 1994)
  - `molecular_weight()`: Calcola il peso molecolare in Daltons (somma dei pesi atomici)

---

## ✅ VERIFICA DEI REQUISITI

### LEVEL 1 - Tutti i requisiti soddisfatti ✅

- [x] **(1) Calcola IEP** - Implementato con `ProteinAnalysis.isoelectric_point()`
- [x] **(2) Calcola MW** - Implementato con `ProteinAnalysis.molecular_weight()`
- [x] **(3) Filtra con AND logic** - Implementato con `(iep_lower <= iep <= iep_upper) and (mw_lower <= mw <= mw_upper)`
- [x] **Usage senza argomenti** - Mostra messaggio di help
- [x] **Output formato corretto** - Stampa header, IEP e MW come richiesto

### LEVEL 2 - Requisito soddisfatto ✅

- [x] **Interfaccia web CGI** - Implementata in `related_IEP_MW.cgi`
- [x] **Visualizza proteine** - Mostra risultati in tabella HTML
- [x] **Form di input** - Permette inserimento criteri di ricerca

---

## 🚀 COME TESTARE LA SOLUZIONE

### Test LEVEL 1
```bash
cd MOCK_EXAM/Exam_Simulation
python related_IEP_MW.py 7 7.1 41000 42000
```

### Test LEVEL 2 (con web_server.py)
```bash
cd MOCK_EXAM/Exam_Simulation
python web_server.py 8001
# Aprire browser su http://localhost:8001/
```

### Test LEVEL 2 (con CGI - richiede server web configurato)
1. Copiare `related_IEP_MW.cgi` in `/var/www/cgi-bin/` (Linux) o directory cgi-bin del server
2. Copiare `index.html` nella directory web
3. Configurare server web per eseguire CGI
4. Accedere via browser

---

## 📦 STRUTTURA FILE

```
MOCK_EXAM/Exam_Simulation/
├── related_IEP_MW.py          ⭐ FILE PRINCIPALE LEVEL 1
├── related_IEP_MW.cgi         ⭐ FILE PRINCIPALE LEVEL 2
├── index.html                  📄 Interfaccia utente web
├── web_server.py               🔧 Server alternativo (per test)
└── SOLUZIONE_ASSIGNMENT.md     📝 Questo documento

MOCK_EXAM/MOCK_EXAM_SOLUTION/CGI/
└── uniprot-all.fasta           🧬 Database proteine (non da consegnare)
```

---

## 📝 NOTE IMPORTANTI

1. **Il file FASTA** (`uniprot-all.fasta`) **NON va consegnato** - è il database fornito
2. **I file COMMENTED** (`related_IEP_MW_COMMENTED.py`, etc.) sono versioni con commenti extra - **non necessari per la consegna**
3. **I file di documentazione** (README.md, etc.) sono utili ma **non obbligatori**
4. **Per la consegna al prof, bastano:**
   - `related_IEP_MW.py` (LEVEL 1)
   - `related_IEP_MW.cgi` (LEVEL 2)
   - `index.html` (per LEVEL 2)

---

## 🎯 RIEPILOGO FILE DA CONSEGNARE

### MINIMUM VIABLE DELIVERY (Solo l'essenziale)
1. ✅ `related_IEP_MW.py` - Soluzione LEVEL 1
2. ✅ `related_IEP_MW.cgi` - Soluzione LEVEL 2
3. ✅ `index.html` - Interfaccia web (per LEVEL 2)

### DELIVERY COMPLETA (Raccomandato)
1. ✅ `related_IEP_MW.py` - Soluzione LEVEL 1
2. ✅ `related_IEP_MW.cgi` - Soluzione LEVEL 2
3. ✅ `index.html` - Interfaccia web
4. ✅ `SOLUZIONE_ASSIGNMENT.md` - Questo documento (spiegazione)

---

**Autore:** Soluzione Assignment PY4BIO 2025  
**Data:** 2025  
**Versione:** 1.0


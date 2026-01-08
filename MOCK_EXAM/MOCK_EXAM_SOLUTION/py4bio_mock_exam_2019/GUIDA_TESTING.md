# 🧪 GUIDA RAPIDA AL TESTING

## ✅ VERIFICA PRELIMINARE (OFFLINE - Funziona sempre)

```bash
# Test 1: Verifica pattern regex (nessuna connessione necessaria)
python test_patterns_offline.py
```

**Output atteso:** `✓ TUTTI I TEST PASSATI!`

---

## 📦 PREREQUISITI

Prima di testare con vere proteine, installa Biopython:

```bash
pip install biopython
```

---

## 🧬 TEST FUNZIONALI (Richiedono internet per ExPASy)

### Test 1: Singolo ID

```bash
python caspases_cutter.py P17405
```

**Output atteso (esempio):**
```
P17405 ASM_HUMAN caspase_1 FLTDLHWD 208 631
```

### Test 2: File con ID Multipli

```bash
python caspases_cutter.py test.set
```

**Output atteso:**
Diverse righe con risultati da 5 proteine (O00238, P17405, Q01814, Q9H3R0, Q9HCP0)

---

## 🌐 TEST INTERFACCIA WEB FLASK

### Avvio

```bash
python caspases_cutter_flask.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000/
 * Debug mode: on
```

### Uso

1. Apri browser: `http://127.0.0.1:5000/`
2. Inserisci ID (uno per riga)
3. Clicca "Find Cleavage Sites"
4. Vedi risultati in tabella

---

## 🖥️ TEST INTERFACCIA CGI

⚠️ Richiede web server (Apache/Nginx) configurato

### Setup Apache (esempio)

```bash
# 1. Installa Apache
sudo apt-get install apache2

# 2. Abilita CGI
sudo a2enmod cgi

# 3. Copia file
sudo cp caspases_cutter_cgi.py /usr/lib/cgi-bin/
sudo chmod +x /usr/lib/cgi-bin/caspases_cutter_cgi.py
sudo cp caspases_form.html /var/www/html/

# 4. Restart Apache
sudo systemctl restart apache2

# 5. Test nel browser
# http://localhost/caspases_form.html
```

---

## 🔍 TEST COMPLETO AUTOMATICO

```bash
python test_caspases.py
```

Questo script verifica:
- ✓ File esistenti
- ✓ Sintassi Python
- ✓ Importazioni moduli
- ✓ Pattern regex
- ✓ Funzioni definite
- ✓ File test.set
- ✓ CGI requirements
- ✓ HTML form
- ✓ Flask setup

---

## ⚠️ TROUBLESHOOTING

### Problema: "Module 'Bio' not found"
**Soluzione:**
```bash
pip install biopython
```

### Problema: "Connection timeout" (ExPASy)
**Cause possibili:**
- ID non valido
- Problemi di rete
- Server UniProt temporaneamente down

**Soluzione:**
Riprova dopo qualche minuto. Se persiste, verifica connessione internet.

### Problema: CGI "500 Internal Server Error"
**Checklist:**
1. ✓ Shebang presente: `#!/usr/bin/env python`
2. ✓ File eseguibile: `chmod +x script.py`
3. ✓ Header HTTP: `print('Content-Type: text/html\n')`
4. ✓ cgitb abilitato: `cgitb.enable()`

**Debug:**
```bash
# Guarda log Apache
tail -f /var/log/apache2/error.log
```

### Problema: Pattern non trova nulla
**Debug:**
```python
import re
pattern = re.compile(r'...D.{4}')
test = "FLTDLHWD"
print(pattern.search(test))  # Dovrebbe restituire un match object
```

---

## 📊 RISULTATI ATTESI (test.set)

Dall'esame, per i 5 ID nel test.set ci si aspetta output come:

```
O00238 BMR1B_HUMAN caspase_1 LITDYHEN 280 502
P17405 ASM_HUMAN caspase_1 FLTDLHWD 208 631
Q01814 AT2B2_HUMAN caspase_1 LPADGLFI 225 1243
Q01814 AT2B2_HUMAN caspase_1 LTTDTSKS 1222 1243
Q9H3R0 KDM4C_HUMAN caspase_1 YGADINGS 137 1056
Q9H3R0 KDM4C_HUMAN caspase_1 YGADIIQG 1014 1056
Q9H3R0 KDM4C_HUMAN caspase_7 DEVDGAEV 396 1056
Q9HCP0 KC1G1_HUMAN caspase_1 LKADTLKE 257 422
Q9HCP0 KC1G1_HUMAN caspase_1 LFTDLFEK 313 422
```

**Nota:** Potrebbero esserci più risultati con il pattern permissivo.

---

## 📝 CHECKLIST FINALE

Prima della consegna:

- [ ] `test_patterns_offline.py` passa (12/12 test)
- [ ] Script base funziona con singolo ID
- [ ] Script base funziona con file
- [ ] Flask si avvia senza errori
- [ ] CGI ha shebang e è eseguibile
- [ ] HTML form punta a path CGI corretto
- [ ] Tutti i file hanno documentazione
- [ ] Codice ben formattato e commentato

---

## 💡 SUGGERIMENTI

1. **Testa offline prima:** Usa `test_patterns_offline.py` per verificare la logica
2. **Un test alla volta:** Non testare tutto insieme, procedi gradualmente
3. **Leggi gli errori:** I messaggi di errore spesso indicano esattamente il problema
4. **Verifica log:** In caso di CGI, i log di Apache sono fondamentali
5. **Chiedi aiuto:** Se bloccato, usa SPIEGAZIONE_COMPLETA.md come riferimento

---

**Buon testing! 🚀**

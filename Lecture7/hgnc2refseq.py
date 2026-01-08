import sqlite3
import sys

def readSqliteTable(HGNC):
    try:
        sqliteConnection = sqlite3.connect('refGene_hg19.db')
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")

        sqlite_select_query = """SELECT name from refGene where name2=?"""
        data=(HGNC,)
        cursor.execute(sqlite_select_query,data)
        records = cursor.fetchall()
        
        refseq_list=[]
        for row in records:
            refseq_list.append(row[0])

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("The SQLite connection is closed")

    return refseq_list

if not len(sys.argv) == 2:
        sys.stderr.write("USAGE: python3 %s < gene symbol e.g. TP53 of file with gene symbols (1 per line) >\n" % sys.argv[0])
        sys.exit(1)

gene_symbol = sys.argv[1]
try:
    with open(gene_symbol) as f:
        print("Processing a list of HGNC symbols...")
        fh = open(gene_symbol, "r")
        for HGNC in fh:
            HGNC = HGNC.rstrip()
            refseq_list = readSqliteTable(HGNC)
            print(HGNC,":",','.join(refseq_list))

except FileNotFoundError:
    print("Dealing with a single gene symbol!!!")
    refseq_list = readSqliteTable(gene_symbol)
    print(gene_symbol,":",','.join(refseq_list))

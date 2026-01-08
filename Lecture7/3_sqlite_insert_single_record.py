import sqlite3
import os
from pathlib import Path

# Ensure the working directory is the directory where this script resides
SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

# Use an explicit path for the database inside Lecture7
DB_PATH = SCRIPT_DIR / 'py4bio_meeting_2025.db'

try:
    sqliteConnection = sqlite3.connect(DB_PATH)
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_speaker = """insert into speaker(first_name,last_name,phone,email) 
                                values('Marie','Curie',987654,'mariec@science-heaven.be');"""

    count = cursor.execute(sqlite_insert_speaker)
    sqliteConnection.commit()
    print("Record inserted successfully into speaker table ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("The SQLite connection is closed")

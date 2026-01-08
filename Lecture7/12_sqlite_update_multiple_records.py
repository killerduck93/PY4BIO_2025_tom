import sqlite3
import os
from pathlib import Path

# Ensure the working directory is the directory where this script resides
SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

# Use an explicit path for the database inside Lecture7
DB_PATH = SCRIPT_DIR / 'py4bio_meeting_2025.db'

def updateMultipleRecords(recordList):
    try:
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_update_query = """Update speaker set phone = ? where speaker_id = ?"""
        cursor.executemany(sqlite_update_query, recordList)
        sqliteConnection.commit()
        print("Total", cursor.rowcount, "Records updated successfully")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update multiple records of sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

records_to_update = [ (12345, 4), (45678, 5), (98765, 6) ]
updateMultipleRecords(records_to_update)

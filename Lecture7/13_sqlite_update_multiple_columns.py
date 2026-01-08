import sqlite3
import os
from pathlib import Path

# Ensure the working directory is the directory where this script resides
SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

# Use an explicit path for the database inside Lecture7
DB_PATH = SCRIPT_DIR / 'py4bio_meeting_2025.db'

def updateMultipleColumns(speaker_id, phone, email):
    try:
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_update_query = """Update speaker set phone = ?, email = ? where speaker_id = ?"""
        columnValues = (phone, email, speaker_id)
        cursor.execute(sqlite_update_query, columnValues)
        sqliteConnection.commit()
        print("Multiple columns updated successfully")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update multiple columns of sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

updateMultipleColumns(5, 66666, 'vlad.dracula@gmail.com')

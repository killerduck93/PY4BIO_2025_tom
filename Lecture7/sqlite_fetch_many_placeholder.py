import sqlite3
import os
from pathlib import Path

# Ensure the working directory is the directory where this script resides
SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

# Use an explicit path for the database inside Lecture7
DB_PATH = SCRIPT_DIR / 'py4bio_meeting_2025.db'

def readLimitedRows(rowSize):
    try:
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from session WHERE description LIKE \"%a%\""""
        cursor.execute(sqlite_select_query)
        print("Reading ", rowSize, " rows")
        records = cursor.fetchmany(rowSize)
        print("Printing each row \n")
        for row in records:
            print("name: ", row[0])
            print("speaker_id: ", row[1])
            print("description: ", row[2])
            print("start: ", row[3])
            print("duration: ", row[4])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

readLimitedRows(2)

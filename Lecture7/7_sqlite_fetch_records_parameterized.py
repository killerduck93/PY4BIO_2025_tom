import sqlite3
import os
from pathlib import Path

# Ensure the working directory is the directory where this script resides
SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

# Use an explicit path for the database inside Lecture7
DB_PATH = SCRIPT_DIR / 'py4bio_meeting_2025.db'

def getSpeakerInfo(speaker_id):
    try:
        sqliteConnection = sqlite3.connect(DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select * from speaker where speaker_id = ?"""
        cursor.execute(sql_select_query, (speaker_id,))
        records = cursor.fetchall()
        print("Printing ID ", speaker_id)
        for row in records:
            print("speaker_id: ", row[0])
            print("first_name: ", row[1])
            print("last_name: ", row[2])
            print("phone: ", row[3])
            print("email: ", row[4])
            print("\n")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

getSpeakerInfo(2)

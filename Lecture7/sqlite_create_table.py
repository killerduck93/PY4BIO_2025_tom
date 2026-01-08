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
    sqlite_create_table_query = '''CREATE TABLE `speaker` (
 	                            `speaker_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                            `first_name`	varchar ( 128 ) NOT NULL,
	                            `last_name`	varchar ( 128 ) NOT NULL,
	                            `phone`	int ( 10 ) NOT NULL,
	                            `email`	varchar ( 255 ) NOT NULL);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")

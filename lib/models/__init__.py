import sqlite3

CONN = sqlite3.connect('tour_schedule.db')
CURSOR = CONN.cursor()

# Create tables if they don't exist
CURSOR.execute('''CREATE TABLE IF NOT EXISTS bands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    genre TEXT NOT NULL
)''')

CURSOR.execute('''CREATE TABLE IF NOT EXISTS tour_dates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_id INTEGER,
    location TEXT NOT NULL,
    date TEXT NOT NULL,
    venue TEXT NOT NULL,
    FOREIGN KEY(band_id) REFERENCES bands(id)
)''')

CONN.commit()

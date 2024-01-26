import sqlite3

conn = sqlite3.connect('phDB.db')
cur = conn.cursor()

try:
    # Create 'bruger' table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bruger (
            bruger_id INTEGER PRIMARY KEY,
            produkt_id TEXT NOT NULL
        )
    ''')

    # Create 'koordinater' table with UNIQUE constraint on 'bruger_id'
    cur.execute('''
        CREATE TABLE IF NOT EXISTS koordinater (
            koordinat_id INTEGER PRIMARY KEY,
            bruger_id INTEGER NOT NULL UNIQUE,
            latitude TEXT,
            longitude TEXT,
            FOREIGN KEY (bruger_id) REFERENCES bruger(bruger_id)
        )
    ''')

    # Create 'faldet' table with UNIQUE constraint on 'bruger_id'
    cur.execute('''
        CREATE TABLE IF NOT EXISTS faldet (
            faldet_id INTEGER PRIMARY KEY,
            bruger_id INTEGER NOT NULL UNIQUE,
            faldet_status INTEGER,
            FOREIGN KEY (bruger_id) REFERENCES bruger(bruger_id)
        )
    ''')

    # Create 'promille' table with UNIQUE constraint on 'bruger_id'
    cur.execute('''
        CREATE TABLE IF NOT EXISTS promille (
            promille_id INTEGER PRIMARY KEY,
            bruger_id INTEGER NOT NULL UNIQUE,
            promille REAL,
            FOREIGN KEY (bruger_id) REFERENCES bruger(bruger_id)
        )
    ''')
except sqlite3.Error as e:
    print(f'Could not create tables! {e}')
finally:
    conn.commit()
    conn.close()
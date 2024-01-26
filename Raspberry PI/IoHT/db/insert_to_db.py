import sqlite3

def insertIntoDB(produkt_id):
    conn = sqlite3.connect('phDB.db')
    bruger_id = None
    query = 'INSERT INTO bruger (produkt_id) VALUES(?)'
    data = (produkt_id,)
    try:
        cur = conn.cursor()
        cur.execute(query, data)
        bruger_id = cur.lastrowid  # Get the last inserted id
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert into bruger ! {e} ')
    finally:
        conn.close()
    return bruger_id

def insertKoordinater(bruger_id, latitude, longitude):
    conn = sqlite3.connect('phDB.db')
    query = 'INSERT INTO koordinater (bruger_id, latitude, longitude) VALUES (?, ?, ?)'
    data = (bruger_id, latitude, longitude)
    try:
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert into koordinater ! {e} ')
    finally:
        conn.close()

def insertPromille(bruger_id, promille_value):
    conn = sqlite3.connect('phDB.db')
    query = 'INSERT INTO promille (bruger_id, promille) VALUES (?, ?)'
    data = (bruger_id, promille_value)
    try:
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert into promille ! {e} ')
    finally:
        conn.close()

def insertFaldet(bruger_id, faldet_status):
    conn = sqlite3.connect('phDB.db')
    query = 'INSERT INTO faldet (bruger_id, faldet_status) VALUES (?, ?)'
    data = (bruger_id, faldet_status)
    try:
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert into faldet ! {e} ')
    finally:
        conn.close()

# Insert test user, coordinates, promille, and faldet
produkt_id = "test1"
bruger_id = insertIntoDB(produkt_id)

if bruger_id:
    # Example data
    latitude = "55.69178"
    longitude = "12.55388"
    promille_value = 0.05  # Example promille value
    faldet_status = 1      # Example faldet status (1 or 0)

    insertKoordinater(bruger_id, latitude, longitude)
    insertPromille(bruger_id, promille_value)
    insertFaldet(bruger_id, faldet_status)

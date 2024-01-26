import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'db', 'phDB.db'))

class Bruger:
    def __init__(self, bruger_id, produkt_id):
        self.bruger_id = bruger_id
        self.produkt_id = produkt_id

    def save(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        if self.bruger_id:
            cur.execute('UPDATE bruger SET produkt_id=? WHERE bruger_id=?', 
                        (self.produkt_id, self.bruger_id))
        else:
            cur.execute('INSERT INTO bruger (produkt_id) VALUES (?)', 
                        (self.produkt_id,))
            self.bruger_id = cur.lastrowid
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM bruger WHERE bruger_id=?', 
                    (self.bruger_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_produkt_id(produkt_id):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM bruger WHERE produkt_id=?', (produkt_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Bruger(row[0], row[1])
        else:
            return None

    @staticmethod
    def get_all():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM bruger')
        rows = cur.fetchall()
        conn.close()
        brugere = []
        for row in rows:
            bruger = Bruger(row[0], row[1])
            brugere.append(bruger)
        return brugere

class Koordinater:
    def __init__(self, koordinat_id, bruger_id, latitude, longitude):
        self.koordinat_id = koordinat_id
        self.bruger_id = bruger_id
        self.latitude = latitude
        self.longitude = longitude

    def save(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        if self.koordinat_id:
            cur.execute('UPDATE koordinater SET bruger_id=?, latitude=?, longitude=? WHERE koordinat_id=?',
                        (self.bruger_id, self.latitude, self.longitude, self.koordinat_id))
        else:
            cur.execute('INSERT INTO koordinater (bruger_id, latitude, longitude) VALUES (?, ?, ?)',
                        (self.bruger_id, self.latitude, self.longitude))
            self.koordinat_id = cur.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_bruger_id(bruger_id):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM koordinater WHERE bruger_id=?', (bruger_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Koordinater(row[0], row[1], row[2], row[3])
        else:
            return None

    @staticmethod
    def find_by_produkt_id(produkt_id):
        bruger = Bruger.find_by_produkt_id(produkt_id)
        if bruger:
            return Koordinater.find_by_bruger_id(bruger.bruger_id)
        else:
            return None

class Faldet:
    @staticmethod
    def find_by_produkt_id(produkt_id):
        bruger = Bruger.find_by_produkt_id(produkt_id)
        if bruger:
            return Faldet.find_by_bruger_id(bruger.bruger_id)
        else:
            return None

    @staticmethod
    def find_by_bruger_id(bruger_id):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT faldet_status FROM faldet WHERE bruger_id=?', (bruger_id,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
    
class Promille:
    @staticmethod
    def find_by_produkt_id(produkt_id):
        bruger = Bruger.find_by_produkt_id(produkt_id)
        if bruger:
            return Promille.find_by_bruger_id(bruger.bruger_id)
        else:
            return None

    @staticmethod
    def find_by_bruger_id(bruger_id):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT promille FROM promille WHERE bruger_id=?', (bruger_id,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
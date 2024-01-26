import sqlite3

def checkIfInsertWorked(produkt_id):
    conn = sqlite3.connect('phDB.db')
    query = 'SELECT * FROM bruger WHERE produkt_id = ?'
    data = (produkt_id,)
    try:
        cur = conn.cursor()
        cur.execute(query, data)
        result = cur.fetchall()
        if result:
            print(f'Record found: {result}')
        else:
            print('No record found with that produkt_id.')
    except sqlite3.Error as e:
        print(f'Error fetching data: {e}')
    finally:
        conn.close()

produkt_id = "test1"
checkIfInsertWorked(produkt_id)
import os
import sqlite3
import encryption
import paho.mqtt.client as mqtt

db_path = db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'db', 'phDB.db'))

def on_message(client, userdata, message):
    data = message.payload.decode("utf-8")

    parts = data.split(" ")
    prod_koord = parts[0]
    lat_long = parts[1].split(",", 1)
    fall_status = parts[2]
    promille = parts[3]


    encrypted_latitude = encryption.encrypt_data(lat_long[0])
    encrypted_longitude = encryption.encrypt_data(lat_long[1])

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
                UPDATE koordinater
                SET latitude = ?, longitude = ?
                WHERE bruger_id = (
                    SELECT bruger_id
                    FROM bruger
                    WHERE produkt_id = ?
                )
                ''', (encrypted_latitude, encrypted_longitude, prod_koord))

    cur.execute('''
                    UPDATE faldet
                    SET faldet_status = ?
                    WHERE bruger_id = (
                        SELECT bruger_id
                        FROM bruger
                        WHERE produkt_id = ?
                    )
                    ''', (fall_status, prod_koord))
    
    cur.execute('''
                    UPDATE promille
                    SET promille = ?
                    WHERE bruger_id = (
                        SELECT bruger_id
                        FROM bruger
                        WHERE produkt_id = ?
                    )
                    ''', (promille, prod_koord))
    conn.commit()
    conn.close()
    print("record inserted.")
    print(f"Received message: {message.payload.decode()}")

def mqtt_listener():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("192.168.4.2", 1883)
    client.subscribe("gps_data_topic")
    client.loop_start()
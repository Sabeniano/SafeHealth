import os
import json
from cryptography.fernet import Fernet

key_path = key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'db', 'key.json'))

def load_encryption_key():
    with open(key_path, 'r') as file:
        data = json.load(file)
        return data['encryption_key'].encode()  # Encode back to bytes

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()

key = load_encryption_key()
cipher_suite = Fernet(key)
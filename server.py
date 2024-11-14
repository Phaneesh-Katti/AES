import socket
import sqlite3
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import json
from datetime import datetime

# config.json
with open("config.json", "r") as f:
    config = json.load(f)

SERVER_HOST = config["SERVER_HOST"]
SERVER_PORT = config["SERVER_PORT"]
PASSWORD = config["PASSWORD"]
DB_FILE = config["DB_FILE"]
KEY_ITERATIONS = config["KEY_ITERATIONS"]

# Key derivation
def derive_key(password, salt=b"SALT12345"):
    return PBKDF2(password, salt, dkLen=32, count=KEY_ITERATIONS)

# AES encryption and decryption
def decrypt_message(encrypted_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(encrypted_data).rstrip(b"\0")

# Database setup
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        user_id BLOB,
        message BLOB,
        iv BLOB,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# def store_message(user_id, message, iv):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO messages (user_id, message, iv, timestamp) VALUES (?, ?, ?, ?)",
#                    (user_id, message, iv, datetime.now()))
#     conn.commit()
#     conn.close()


def store_message(user_id, message, iv):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat() 
    cursor.execute("INSERT INTO messages (user_id, message, iv, timestamp) VALUES (?, ?, ?, ?)",
                   (user_id, message, iv, timestamp))
    conn.commit()
    conn.close()


# Server setup
def start_server():
    setup_database()
    key = derive_key(PASSWORD)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} established.")
            
            try:
                iv = client_socket.recv(16)  # Receive IV
                encrypted_username = client_socket.recv(16)  # Receive encrypted username
                encrypted_message = client_socket.recv(1024)  # Receive encrypted message
                
                # Decrypt the username and message
                username = decrypt_message(encrypted_username, key, iv).decode()
                message = decrypt_message(encrypted_message, key, iv).decode()
                
                # Store the encrypted data
                store_message(encrypted_username, encrypted_message, iv)
                
                print(f"Received message from {username}: {message}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client_socket.close()

if __name__ == "__main__":
    start_server()


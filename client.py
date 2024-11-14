import socket
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import json


# config.json
with open("config.json", "r") as f:
    config = json.load(f)

SERVER_HOST = config["SERVER_HOST"]
SERVER_PORT = config["SERVER_PORT"]
PASSWORD = config["PASSWORD"]
KEY_ITERATIONS = config["KEY_ITERATIONS"]

def derive_key(password, salt=b"SALT12345"):
    return PBKDF2(password, salt, dkLen=32, count=KEY_ITERATIONS)

def encrypt_message(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = message + b"\0" * (16 - len(message) % 16)  # Padding for AES block size
    return cipher.encrypt(padded_message)

def send_message(username, message):
    key = derive_key(PASSWORD)
    iv = get_random_bytes(16)  # Random IV for each message
    print(f"iv = {iv}\n")

    # Encrypt username and message
    encrypted_username = encrypt_message(username.encode(), key, iv)
    encrypted_message = encrypt_message(message.encode(), key, iv)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(iv)  # Send IV
        client_socket.sendall(encrypted_username[:16])  # Send encrypted username (16 bytes)
        client_socket.sendall(encrypted_message)  # Send encrypted message

if __name__ == "__main__":
    username = input("Enter username: ")
    message = input("Enter message: ")
    send_message(username, message)

import socket
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import json

# SERVER_HOST = '127.0.0.1'
# SERVER_PORT = 1234
# PASSWORD = "COL759"
# KEY_ITERATIONS = 100000

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


# import json
# import socket
# from Crypto.Cipher import AES
# from Crypto.Protocol.KDF import PBKDF2
# import os
# from Crypto.Util.Padding import pad

# # Load configurations from config.json
# with open("config.json", "r") as f:
#     config = json.load(f)

# SERVER_HOST = config["SERVER_HOST"]
# SERVER_PORT = config["SERVER_PORT"]
# PASSWORD = config["PASSWORD"]
# KEY_ITERATIONS = config["KEY_ITERATIONS"]
# SALT = config["SALT"].encode()

# def derive_key(password, salt):
#     return PBKDF2(password, salt, dkLen=32, count=KEY_ITERATIONS)

# def main():
#     username = input("Enter your username: ").ljust(16)[:16]  # Fixed 16-byte username
#     message = input("Enter your message: ")

#     key = derive_key(PASSWORD, SALT)
#     iv = os.urandom(16)

#     # Encrypt with padding
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     encrypted_user_id = cipher.encrypt(pad(username.encode(), AES.block_size))
#     encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))

#     # Connect to server and send data
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((SERVER_HOST, SERVER_PORT))

#     client_socket.sendall(iv)
#     client_socket.sendall(encrypted_user_id)
#     client_socket.sendall(encrypted_message)

#     client_socket.close()
#     print("Message sent to server.")

# if __name__ == "__main__":
#     main()


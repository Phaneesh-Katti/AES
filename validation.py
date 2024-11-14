import sqlite3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import json


# Load configurations from config.json
with open("config.json", "r") as f:
    config = json.load(f)

PASSWORD = config["PASSWORD"]
DB_FILE = config["DB_FILE"]
KEY_ITERATIONS = config["KEY_ITERATIONS"]

# Key derivation function
def derive_key(password, salt=b"SALT12345"):
    return PBKDF2(password, salt, dkLen=32, count=KEY_ITERATIONS)

# AES decryption with padding removal
def decrypt_message(encrypted_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data.rstrip(b"\0")

# Connect to database
# conn = sqlite3.connect("SQLITE.db")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Key derivation
key = derive_key(PASSWORD)

print("Validation script to show raw encrypted data and its decrypted version...\n")

# Retrieve row wise message?
for row in cursor.execute("SELECT id, user_id, message, iv, timestamp FROM messages"):
    message_id, encrypted_user_id, encrypted_message, iv, timestamp = row
    
    print(f"--- Entry ID: {message_id} ---\n")
    print("Raw Encrypted Data:")
    print(f"  Encrypted Username (user_id): {encrypted_user_id}")
    print(f"  Encrypted Message: {encrypted_message}")
    print(f"  IV: {iv}")
    print(f"  Timestamp: {timestamp}")

    # Decrypt the user_id and message
    try:
        user_id = decrypt_message(encrypted_user_id, key, iv).decode()
        message = decrypt_message(encrypted_message, key, iv).decode()
        print("\nDecrypted Data:")
        print(f"  Username: {user_id}")
        print(f"  Message: {message}")
    except Exception as e:
        print(f"  Error decrypting message: {e}")

    print("-" * 40 + "\n")

conn.close()

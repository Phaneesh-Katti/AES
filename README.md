## Secure Messaging Application

### Folder Contents
1. **server.py** - Script to run the messaging server.
2. **client.py** - Script for the client to send encrypted messages to the server.
3. **validation.py** - Script to validate and decrypt stored messages for verification purposes.
4. **config.json** - Configuration file with server and encryption settings.

### Prerequisites
- Python 3.x
- Required Python packages: `pycryptodome` (for cryptographic operations)

   To install dependencies, run:
   ```
   pip install pycryptodome
   ```

### Configuration
Ensure the `config.json` file is correctly set with the following fields:
- `"SERVER_HOST"` - IP address of the server (e.g., `"127.0.0.1"`).
- `"SERVER_PORT"` - Port number (e.g., `1234`).
- `"PASSWORD"` - Password for key derivation.
- `"DB_FILE"` - SQLite database file name (e.g., `"SQLITE.db"`).
- `"KEY_ITERATIONS"` - Number of iterations for key derivation (e.g., `100000`).

### How to Run

1. **Start the Server**
   - Run `server.py` to start the server:
     ```
     python server.py
     ```
   - The server will begin listening for incoming client connections.

2. **Send a Message from the Client**
   - Run `client.py` and follow the prompts to enter a username and message:
     ```
     python client.py
     ```
   - The client encrypts the message and sends it to the server. The server then stores the encrypted message, username, and IV in the database.

3. **Validate Stored Messages (Optional)**
   - To view and decrypt stored messages in the database, run `validation.py`:
     ```
     python validation.py
     ```
   - This script will output both the encrypted data and the decrypted (original) messages for verification.

### Notes
- Ensure `server.py` is running before starting `client.py`.
- Each message and username is encrypted with a unique IV for security.
- Modify the settings in `config.json` as needed for your environment.

--- 

import socket, os, time
from crypto_utils import encrypt_data, sha256_hash

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9001
CHUNK_SIZE = 1024

def send_file(filename):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to receiver at {SERVER_IP}:{SERVER_PORT}")
    except ConnectionRefusedError:
        print("Connection refused.")
        return

    # Authentication
    s.send(b"C9B9dsiasZQmY7d")
    auth_response = s.recv(1024).decode()
    if auth_response != "AUTH_OK":
        print("Authentication failed.")
        return

    with open(filename, 'rb') as f:
        raw_data = f.read()

    encrypted_data = encrypt_data(raw_data)
    file_hash = sha256_hash(raw_data)

    total_parts = len(encrypted_data) // CHUNK_SIZE + (len(encrypted_data) % CHUNK_SIZE != 0)
    meta = f"{os.path.basename(filename)}|{total_parts}|{file_hash}"
    s.send(meta.encode())

    ack = s.recv(3)
    if ack != b'ACK':
        print("Receiver did not acknowledge.")
        s.close()
        return

    for part_num in range(total_parts):
        chunk = encrypted_data[part_num * CHUNK_SIZE : (part_num + 1) * CHUNK_SIZE]
        header = f"{part_num:06}".encode()
        s.send(header + chunk)
        time.sleep(0.01)

    s.close()
    print("File transfer completed.")

if __name__ == "__main__":
    send_file("CV.pdf")

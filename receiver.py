import socket
from crypto_utils import decrypt_data, sha256_hash

LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 9001
CHUNK_SIZE = 1024
AUTH_PASSWORD = "C9B9dsiasZQmY7d"

def receive_file():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LISTEN_IP, LISTEN_PORT))
    s.listen(1)
    print("Waiting for connection...")

    conn, addr = s.accept()
    print(f"Connection from {addr}")

    # Step 1: Authentication
    password = conn.recv(1024).decode()
    if password != AUTH_PASSWORD:
        conn.send(b'AUTH_FAIL')
        conn.close()
        print("Authentication failed.")
        return
    conn.send(b'AUTH_OK')

    # Step 2: Receive metadata
    meta = conn.recv(1024).decode()
    if '|' not in meta:
        print(f"Invalid metadata: {meta}")
        conn.close()
        return

    filename, total_parts, file_hash = meta.split('|')
    total_parts = int(total_parts)

    conn.send(b'ACK')
    print(f"Receiving {filename} in {total_parts} parts...")

    received_chunks = [None] * total_parts
    while None in received_chunks:
        data = conn.recv(CHUNK_SIZE + 6)
        part_num = int(data[:6].decode())
        content = data[6:]
        received_chunks[part_num] = content

    encrypted_data = b''.join(received_chunks)

    try:
        decrypted_data = decrypt_data(encrypted_data)
    except Exception as e:
        print(f"Decryption failed: {e}")
        return

    # Step 3: Verify hash
    calculated_hash = sha256_hash(decrypted_data)
    if calculated_hash != file_hash:
        print("File integrity check failed!")
    else:
        print("Integrity verified.")

    with open("received_" + filename, 'wb') as f:
        f.write(decrypted_data)

    print(f"File saved as received_{filename}")
    conn.close()
    s.close()

if __name__ == "__main__":
    receive_file()

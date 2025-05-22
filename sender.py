import socket
import os
import time
from crypto_utils import encrypt_data, sha256_hash
from network_utils import check_network_conditions

SERVER_IP = '127.0.0.1'
TCP_PORT = 9001
UDP_PORT = 9002
CHUNK_SIZE = 1024
AUTH_PASSWORD = b"C9B9dsiasZQmY7d"

def send_file_tcp(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((SERVER_IP, TCP_PORT))
        print(f"[TCP] Connected to receiver at {SERVER_IP}:{TCP_PORT}")
    except ConnectionRefusedError:
        print("[TCP] Connection refused.")
        return

    s.send(AUTH_PASSWORD)
    auth_response = s.recv(1024)
    if auth_response != b"AUTH_OK":
        print("[TCP] Authentication failed.")
        s.close()
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
        print("[TCP] Receiver did not acknowledge.")
        s.close()
        return

    for part_num in range(total_parts):
        chunk = encrypted_data[part_num * CHUNK_SIZE : (part_num + 1) * CHUNK_SIZE]
        header = f"{part_num:06}".encode()
        s.send(header + chunk)
        time.sleep(0.01)

    s.close()
    print("[TCP] File transfer completed.")

def send_file_udp(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(3)
    try:
        with open(filename, 'rb') as f:
            raw_data = f.read()
    except FileNotFoundError:
        print("[UDP] File not found.")
        return

    encrypted_data = encrypt_data(raw_data)
    file_hash = sha256_hash(raw_data)
    total_parts = len(encrypted_data) // CHUNK_SIZE + (len(encrypted_data) % CHUNK_SIZE != 0)
    meta = f"{os.path.basename(filename)}|{total_parts}|{file_hash}"

    # Send meta and wait for ACK
    s.sendto(meta.encode(), (SERVER_IP, UDP_PORT))
    try:
        data, _ = s.recvfrom(1024)
        if data != b'ACK':
            print("[UDP] Receiver did not acknowledge meta.")
            s.close()
            return
    except socket.timeout:
        print("[UDP] No ACK received for meta.")
        s.close()
        return

    # Send data packets
    for part_num in range(total_parts):
        chunk = encrypted_data[part_num * CHUNK_SIZE : (part_num + 1) * CHUNK_SIZE]
        header = f"{part_num:06}".encode()
        packet = header + chunk
        s.sendto(packet, (SERVER_IP, UDP_PORT))
        time.sleep(0.005)

    s.close()
    print("[UDP] File transfer completed.")

def send_file_hybrid(filename, mode="auto"):
    print("Checking network conditions...")
    if mode == "tcp":
        print("User selected TCP mode.")
        send_file_tcp(filename)
    elif mode == "udp":
        print("User selected UDP mode.")
        send_file_udp(filename)
    else:
        # Otomatik seçim
        if check_network_conditions(SERVER_IP):
            print("Network good. Using UDP mode.")
            send_file_udp(filename)
        else:
            print("Network bad. Using TCP mode.")
            send_file_tcp(filename)

if __name__ == "__main__":
    # Örnek çağrı: otomatik mod
    send_file_hybrid("CV.pdf", mode="auto")

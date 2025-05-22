import socket
import threading
from crypto_utils import decrypt_data, sha256_hash

LISTEN_IP = '127.0.0.1'
TCP_PORT = 9001
UDP_PORT = 9002
CHUNK_SIZE = 1024
AUTH_PASSWORD = b"C9B9dsiasZQmY7d"

def receive_file_tcp():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LISTEN_IP, TCP_PORT))
    s.listen(1)
    print("[TCP] Bağlantı bekleniyor...")

    conn, addr = s.accept()
    print(f"[TCP] Bağlantı alındı: {addr}")

    password = conn.recv(1024)
    if password != AUTH_PASSWORD:
        conn.send(b'AUTH_FAIL')
        conn.close()
        print("[TCP] Doğrulama başarısız.")
        return
    conn.send(b'AUTH_OK')

    meta = conn.recv(1024).decode()
    if '|' not in meta:
        print(f"[TCP] Geçersiz metadata: {meta}")
        conn.close()
        return

    filename, total_parts, file_hash = meta.split('|')
    total_parts = int(total_parts)

    conn.send(b'ACK')
    print(f"[TCP] {filename} dosyası, {total_parts} parçada alınıyor...")

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
        print(f"[TCP] Şifre çözme başarısız: {e}")
        return

    calculated_hash = sha256_hash(decrypted_data)
    if calculated_hash != file_hash:
        print("[TCP] Dosya bütünlük kontrolü başarısız!")
    else:
        print("[TCP] Bütünlük doğrulandı.")

    with open("received_tcp_" + filename, 'wb') as f:
        f.write(decrypted_data)

    print(f"[TCP] Dosya kaydedildi: received_tcp_{filename}")
    conn.close()
    s.close()

def receive_file_udp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((LISTEN_IP, UDP_PORT))
    print("[UDP] Veri bekleniyor...")

    # Meta bilgisi alma
    meta, addr = s.recvfrom(1024)
    meta = meta.decode()
    if '|' not in meta:
        print(f"[UDP] Geçersiz metadata: {meta}")
        return

    filename, total_parts, file_hash = meta.split('|')
    total_parts = int(total_parts)

    s.sendto(b'ACK', addr)
    print(f"[UDP] {filename} dosyası, {total_parts} parçada alınıyor...")

    received_chunks = [None] * total_parts
    while None in received_chunks:
        try:
            data, _ = s.recvfrom(CHUNK_SIZE + 6)
            part_num = int(data[:6].decode())
            content = data[6:]
            received_chunks[part_num] = content
        except socket.timeout:
            print("[UDP] Paket alımında zaman aşımı.")
            break

    encrypted_data = b''.join([chunk for chunk in received_chunks if chunk])

    try:
        decrypted_data = decrypt_data(encrypted_data)
    except Exception as e:
        print(f"[UDP] Şifre çözme başarısız: {e}")
        return

    calculated_hash = sha256_hash(decrypted_data)
    if calculated_hash != file_hash:
        print("[UDP] Dosya bütünlük kontrolü başarısız!")
    else:
        print("[UDP] Bütünlük doğrulandı.")

    with open("received_udp_" + filename, 'wb') as f:
        f.write(decrypted_data)

    print(f"[UDP] Dosya kaydedildi: received_udp_{filename}")
    s.close()

if __name__ == "__main__":
    # Hem TCP hem UDP alıcılarını ayrı threadlerde çalıştır
    tcp_thread = threading.Thread(target=receive_file_tcp, daemon=True)
    udp_thread = threading.Thread(target=receive_file_udp, daemon=True)

    tcp_thread.start()
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()

import subprocess
import threading
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(name):
    path = os.path.join(BASE_DIR, name)
    subprocess.run(["python", path])

def run_checksum_script():
    print("\n--- Checksum Hesaplama ---")
    run_script("calculate_ip_checksum.py")

def run_send_custom_packet():
    print("\n--- Özelleştirilmiş IP Paketi Gönderimi ---")
    run_script("send_custom_ip_packet.py")

def run_fragment_sender():
    print("\n--- Parçalanmış Paket Gönderimi ---")
    run_script("fragment_and_send.py")

def run_reassembler():
    print("\n--- Fragment Dinleme ve Yeniden Birleştirme ---")
    run_script("reassemble_fragments.py")

if __name__ == "__main__":
    reassembler_thread = threading.Thread(target=run_reassembler, daemon=True)
    reassembler_thread.start()

    time.sleep(3) 

    run_checksum_script()
    time.sleep(1)

    run_send_custom_packet()
    time.sleep(1)

    run_fragment_sender()

    print("\nTüm işlemler tamamlandı. Fragment birleştirme arka planda çalışıyor (CTRL+C ile çıkabilirsiniz).")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram sonlandırıldı.")

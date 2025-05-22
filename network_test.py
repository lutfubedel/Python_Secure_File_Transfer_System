import subprocess
import time
import os
import platform
import threading

from sender import send_file_hybrid

FILE_TO_SEND = "CV.pdf"
RECEIVER_SCRIPT = "receiver.py"
IPERF_PATH = "C:\\Users\\ltfmu\\OneDrive\\Masaüstü\\Bilgisayar_Ağları_Projesi\\secure_file_transfer\\iperf3\\iperf3.exe"
IPERF_SERVER_IP = "127.0.0.1"

def run_ping_test(target, count=4):
    cmd = ["ping", "-n", str(count), target] if platform.system() == "Windows" else ["ping", "-c", str(count), target]
    print(f"\n📶 Pinging {target}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

def run_bandwidth_test(server_ip):
    print(f"\n📊 iPerf3 bandwidth test to {server_ip}")
    result = subprocess.run([IPERF_PATH, "-c", server_ip, "-t", "5"], capture_output=True, text=True)
    print(result.stdout)

def start_receiver():
    os.system(f"start cmd /k python {RECEIVER_SCRIPT}")

def start_iperf_server():
    os.system(f"start cmd /k \"{IPERF_PATH}\" -s")

def main():
    print("📡 Ağ Performans ve Dosya Transfer Testi Başlıyor...\n")

    # 1. Alıcıyı başlat (farklı terminalde)
    print("[🔄] Receiver script başlatılıyor...")
    threading.Thread(target=start_receiver).start()
    time.sleep(2)

    # 2. iPerf3 sunucusunu başlat
    print("[🚀] iPerf3 server başlatılıyor...")
    threading.Thread(target=start_iperf_server).start()
    time.sleep(2)

    # 3. Ping testi
    run_ping_test("127.0.0.1")

    # 4. iPerf testi
    run_bandwidth_test(IPERF_SERVER_IP)

    # 5. Dosya transfer süresi ölç
    print(f"\n📤 {FILE_TO_SEND} dosyası gönderiliyor...")
    start_time = time.time()
    send_file_hybrid(FILE_TO_SEND)
    end_time = time.time()

    print(f"⏱️ Aktarım süresi: {end_time - start_time:.2f} saniye")
    print("✅ Tüm testler tamamlandı.")

if __name__ == "__main__":
    main()

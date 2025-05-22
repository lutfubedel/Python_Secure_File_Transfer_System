import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
import time
import platform
from sender import send_file_hybrid  # Fonksiyonunuzun ismi bu

# Ayarlar
RECEIVER_SCRIPT = "receiver.py"
IPERF_PATH = "C:\\Users\\ltfmu\\OneDrive\\Masaüstü\\Bilgisayar_Ağları_Projesi\\secure_file_transfer\\iperf3\\iperf3.exe"
IPERF_SERVER_IP = "127.0.0.1"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  

class FileTransferApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔒 Secure File Transfer (Modern GUI)")
        self.geometry("850x700")  # biraz daha yüksek
        self.file_path = None

        # Başlık
        ctk.CTkLabel(self, text="🔒 Secure File Transfer", font=("Segoe UI", 24, "bold")).pack(pady=20)

        # Düğmeler
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="📁 Select File", command=self.select_file).grid(row=0, column=0, padx=15)
        ctk.CTkButton(button_frame, text="🚀 Start Transfer", command=self.start_transfer_thread).grid(row=0, column=1, padx=15)

        # Transfer Mode seçim radio buttonları
        mode_frame = ctk.CTkFrame(self)
        mode_frame.pack(pady=10)

        self.transfer_mode = ctk.StringVar(value="auto")  # varsayılan otomatik

        ctk.CTkLabel(mode_frame, text="Transfer Mode:", font=("Segoe UI", 14)).grid(row=0, column=0, padx=10)
        ctk.CTkRadioButton(mode_frame, text="TCP", variable=self.transfer_mode, value="tcp").grid(row=0, column=1, padx=10)
        ctk.CTkRadioButton(mode_frame, text="UDP", variable=self.transfer_mode, value="udp").grid(row=0, column=2, padx=10)
        ctk.CTkRadioButton(mode_frame, text="Auto (Hybrid)", variable=self.transfer_mode, value="auto").grid(row=0, column=3, padx=10)

        # Dosya etiketi
        self.file_label = ctk.CTkLabel(self, text="No file selected", text_color="#aaaaaa", font=("Segoe UI", 11))
        self.file_label.pack(pady=10)

        # Scrollable log container
        self.log_scroll = ctk.CTkScrollableFrame(self, width=780, height=450, fg_color="#1e1e2f")
        self.log_scroll.pack(pady=10)
        self.log_container = self.log_scroll

    def add_output(self, message, emoji="💬", color="#cccccc"):
        frame = ctk.CTkFrame(self.log_container, fg_color="#2a2a3d", corner_radius=6)
        frame.pack(fill="x", padx=10, pady=4)

        label = ctk.CTkLabel(
            frame,
            text=f"{emoji} {message}",
            text_color=color,
            anchor="w",
            font=("Segoe UI", 11)
        )
        label.pack(fill="x", padx=10, pady=6)

    def select_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.file_path = file
            self.file_label.configure(text=f"📄 {os.path.basename(file)}")
            self.add_output(f"Selected file: {file}", emoji="📂", color="#87cefa")

    def run_ping_test(self, target="127.0.0.1", count=4):
        self.add_output("Running ping test...", emoji="📶")
        cmd = ["ping", "-n", str(count), target] if platform.system() == "Windows" else ["ping", "-c", str(count), target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.add_output("Ping test completed.", emoji="✅", color="#a0ffa0")
        for line in result.stdout.strip().splitlines()[-2:]:
            self.add_output(line.strip(), emoji="↪️", color="#aaaaaa")

    def run_bandwidth_test(self):
        self.add_output("Running iPerf3 test...", emoji="📊")
        result = subprocess.run([IPERF_PATH, "-c", IPERF_SERVER_IP, "-t", "5"], capture_output=True, text=True)
        self.add_output("iPerf3 test completed.", emoji="✅", color="#a0ffa0")
        for line in result.stdout.strip().splitlines()[-2:]:
            self.add_output(line.strip(), emoji="↪️", color="#aaaaaa")

    def start_receiver(self):
        os.system(f"start cmd /k python {RECEIVER_SCRIPT}")
        self.add_output("Receiver started successfully.", emoji="🟢", color="#a0ffa0")

    def start_iperf_server(self):
        os.system(f"start cmd /k \"{IPERF_PATH}\" -s")
        self.add_output("iPerf3 server started.", emoji="🛰️", color="#87cefa")

    def start_transfer_thread(self):
        if not self.file_path:
            messagebox.showwarning("No file selected", "Please select a file first.")
            return
        threading.Thread(target=self.perform_transfer).start()

    def perform_transfer(self):
        mode = self.transfer_mode.get()
        self.add_output(f"Starting full transfer process in mode: {mode}", emoji="🔄", color="#00ffff")
        self.start_receiver()
        time.sleep(2)
        self.start_iperf_server()
        time.sleep(2)
        self.run_ping_test()
        self.run_bandwidth_test()

        self.add_output(f"Sending file: {self.file_path}", emoji="📤", color="#87cefa")
        start_time = time.time()

        # Transfer işlemi, mod parametresi gönderiliyor
        send_file_hybrid(self.file_path, mode=mode)

        end_time = time.time()
        duration = end_time - start_time
        self.add_output(f"File sent in {duration:.2f} seconds.", emoji="✅", color="#a0ffa0")
        self.add_output("All tasks completed successfully.", emoji="🎉", color="#00ffcc")

if __name__ == "__main__":
    app = FileTransferApp()
    app.mainloop()

from scapy.all import IP, Raw, sniff
from collections import defaultdict

received_fragments = defaultdict(dict)

def reassemble_packet(packet):
    if IP in packet and Raw in packet:
        ip_layer = packet[IP]
        key = (ip_layer.src, ip_layer.dst, ip_layer.id)
        received_fragments[key][ip_layer.frag] = bytes(packet[Raw].load)

        if ip_layer.flags == 0:  # Son parça
            try:
                full_data = b''.join(received_fragments[key][i] for i in sorted(received_fragments[key]))
                print(f"\n Yeniden birleştirilen veri:\n{full_data.decode(errors='ignore')}")
            except Exception as e:
                print(f"Hata: {e}")

print("Paketler dinleniyor...")
sniff(filter="ip", prn=reassemble_packet)

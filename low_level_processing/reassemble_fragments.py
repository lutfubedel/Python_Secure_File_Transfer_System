from scapy.all import sniff, IP
from collections import defaultdict

# Tüm fragment'ları bu dict'te tutacağız
fragments_dict = defaultdict(list)

def is_my_packet(pkt):
    if IP in pkt:
        ip_layer = pkt[IP]
        # SADECE belirli source IP'den gelenleri işle
        return ip_layer.src == "127.0.0.1"
    return False

def packet_handler(pkt):
    if not is_my_packet(pkt):
        return  # Diğerlerini atla

    ip_layer = pkt[IP]
    ip_id = ip_layer.id
    src = ip_layer.src
    dst = ip_layer.dst
    key = (ip_id, src, dst)

    fragments_dict[key].append(ip_layer)

    # "More Fragments" flag yoksa ve offset == 0 ise tek parça paket
    if ip_layer.flags == 0 and ip_layer.frag == 0:
        print("\n Tek paket veri:", bytes(ip_layer.payload).decode(errors="ignore"))
        return

    # Eğer "More Fragments" = 0 ve offset > 0 => son fragment geldi
    if ip_layer.flags == 0:
        all_frags = fragments_dict[key]
        # Offset'e göre sırala
        all_frags.sort(key=lambda p: p.frag)

        full_payload = b''.join(bytes(f.payload) for f in all_frags)
        try:
            print("\n Yeniden birleştirilen veri:\n", full_payload.decode(errors="ignore"))
        except Exception as e:
            print("Veri birleştirme hatası:", e)

        del fragments_dict[key]  # Belleği temizle

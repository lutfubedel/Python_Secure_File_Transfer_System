from scapy.all import IP, Raw, send

ip_packet = IP(dst="192.168.1.100")  
ip_packet.ttl = 64
ip_packet.flags = "DF"
ip_packet.id = 12345
ip_packet.proto = 6  

packet = ip_packet / Raw(load=b"Merhaba, bu bir test verisidir.")
send(packet)

print("Paket gönderildi.")

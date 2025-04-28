from scapy.all import IP, Raw, send

data = b"A" * 4000 
fragments = []
offset = 0
frag_size = 1400

while offset < len(data):
    chunk = data[offset:offset + frag_size]
    mf_flag = 1 if offset + frag_size < len(data) else 0
    frag_packet = IP(dst="192.168.1.100", id=5555, flags=mf_flag, frag=offset // 8) / Raw(load=chunk)
    fragments.append(frag_packet)
    offset += frag_size

for frag in fragments:
    send(frag)

print("Parçalanmış paketler gönderildi.")

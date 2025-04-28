from scapy.all import IP

def compute_checksum(header_bytes):
    if len(header_bytes) % 2 != 0:
        header_bytes += b'\x00'
    
    total = 0
    for i in range(0, len(header_bytes), 2):
        word = (header_bytes[i] << 8) + header_bytes[i+1]
        total += word
    
    while (total >> 16):
        total = (total & 0xFFFF) + (total >> 16)

    return ~total & 0xFFFF

ip = IP(dst="192.168.1.100", ttl=64)
header_bytes = bytes(ip)
checksum = compute_checksum(header_bytes)

print(f"Hesaplanan Checksum: {hex(checksum)}")

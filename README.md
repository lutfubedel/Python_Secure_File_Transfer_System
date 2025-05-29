# Python_Secure_File_Transfer_System
 
Bu proje, şifrelenmiş dosya aktarımı gerçekleştiren, IP başlığını düşük seviyede işleyebilen ve ağ performansını analiz edebilen ileri düzey bir dosya transfer sistemidir. Hem güvenlik hem de ağ protokolleri açısından detaylı bir mühendislik sunar.

## 🎯 Amaç

- Güvenli, şifreli ve parça bazlı dosya transferi gerçekleştirmek (AES + SHA-256)
- TCP/UDP tabanlı gönderim seçenekleri sunmak ve otomatik protokol seçimi yapmak
- IP başlığı seviyesinde TTL, fragment, checksum gibi alanları elle düzenlemek
- iPerf3 ve Ping gibi araçlarla ağ performansını analiz etmek
- MITM saldırı senaryoları üzerinden sistem güvenliğini test etmek

## 🛠️ Teknolojik Bileşenler

- Python (socket, threading, cryptography, scapy)
- iPerf3 (ağ bant genişliği ölçümü)
- Wireshark (paket analizi)
- Scapy (IP header düzeyinde işlem)
- AES şifreleme (CBC mode)
- SHA-256 ile veri bütünlüğü doğrulama
- GUI (Tkinter ile arayüz)

## 📁 Proje Dosya Yapısı

```
├── sender.py              # Dosya şifreleme ve gönderim (TCP/UDP)
├── receiver.py            # Dosya alma, şifre çözme ve doğrulama
├── crypto_utils.py        # AES şifreleme ve SHA-256 fonksiyonları
├── low_level_processing
    ├── send_custom_ip_packet.py
    ├── fragment_and_send.py
    ├── reassemble_fragments.py
    ├── calculate_ip_checksum.py
├── main.py                # IP düzeyinde tüm testleri sırayla çalıştıran script
├── network_test.py        # iPerf3 ve ping testlerini çalıştırır
├── network_utils.py       # Ağ durumu değerlendirme (ping packet loss)
├── file_transfer_gui.py   # Kullanıcı arayüzü
```

## 🔐 Güvenlik Özellikleri

- **AES-128 CBC Mode** ile şifreleme (IV + Padding)
- **SHA-256** hash kontrolü
- Kimlik doğrulama (sabit şifre ile)
- MITM saldırılarına karşı koruma (Wireshark analizleriyle test edildi)

## 🌐 IP Header İşleme

`scapy` kütüphanesi ile:
- TTL, ID, Flags, Fragment Offset alanları elle ayarlanabilir
- IP header checksum hesaplanabilir
- Paket parçalama (fragmentation) ve birleştirme (reassembly) yapılabilir

## 📊 Ağ Performans Ölçümü

- **Ping**: Gecikme süresi analizi
- **iPerf3**: Bant genişliği testi (5 saniyelik)
- **Zamanlama**: Dosya gönderim süreleri ölçülür

## 💡 Özellikler

- **TCP/UDP Hibrit Gönderim**: Kullanıcıya veya ağ durumuna göre otomatik seçim
- **GUI**: Kolay dosya seçimi, IP girişi ve protokol tercihi
- **Gerçek zamanlı hata kontrolü**

## Youtube Videosu
https://youtu.be/tzg9fCFOfzc

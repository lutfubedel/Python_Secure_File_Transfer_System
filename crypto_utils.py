from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib

KEY = b'C9B9dsiasZQmY7da'

def encrypt_data(data):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted 

def decrypt_data(data):
    iv = data[:16]
    encrypted = data[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted

def sha256_hash(data):
    return hashlib.sha256(data).hexdigest()

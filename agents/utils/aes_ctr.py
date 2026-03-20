from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad, unpad
import hashlib

def encrypt(pwd: str, data: str):
    """加密"""
    salt = b'salt'
    iv = bytes(16)
    key = hashlib.scrypt(pwd.encode(), salt=salt, n=16384, r=8, p=1, dklen=24)
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(data.encode(), 16)).hex()  

def decrypt(pwd: str, encrypted_hex: str):
    """解密"""
    salt = b'salt'
    iv = bytes(16)
    key = hashlib.scrypt(pwd.encode(), salt=salt, n=16384, r=8, p=1, dklen=24)
    return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(bytes.fromhex(encrypted_hex)), 16).decode()  

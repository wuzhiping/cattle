from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import hashlib

def encrypt(pwd: str, data: str):
    """加密"""
    salt = b'salt'
    iv = bytes(8)
    key = hashlib.scrypt(pwd.encode(), salt=salt, n=16384, r=8, p=1, dklen=24)[:16]
    return Blowfish.new(key, Blowfish.MODE_CBC, iv).encrypt(pad(data.encode(), 8)).hex()

def decrypt(pwd: str, encrypted_hex: str):
    """解密"""
    salt = b'salt'
    iv = bytes(8)
    key = hashlib.scrypt(pwd.encode(), salt=salt, n=16384, r=8, p=1, dklen=24)[:16]
    return unpad(Blowfish.new(key, Blowfish.MODE_CBC, iv).decrypt(bytes.fromhex(encrypted_hex)), 8).decode()
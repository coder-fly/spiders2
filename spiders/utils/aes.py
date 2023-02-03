import base64
import json

from Crypto.Cipher import AES

zero_padding = lambda s: s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def pkcs7_unpadding(data):
    pad_len = data[-1]
    data = data[:-pad_len]
    return data


def pkcs7_padding(data, pad_len=16):
    if not isinstance(data, bytes):
        data = data.encode()
    pad_len = pad_len - (len(data) % pad_len)
    data += bytes([pad_len] * pad_len)
    return data


def encrypt(key, text):
    text = pkcs7_padding(text.encode('utf-8'))
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(text)).decode()


def decrypt(key, text):
    text = pkcs7_padding(text.encode('utf-8'))
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    plaintext = base64.b64decode(text)
    return pkcs7_unpadding(cipher.decrypt(plaintext)).decode()

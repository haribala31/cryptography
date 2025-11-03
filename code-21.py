from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
def pad(data, block_size=16):
    padding_len = block_size - (len(data) % block_size)
    if padding_len == 0:
        padding_len = block_size
    return data + bytes([0x80]) + bytes(padding_len - 1)
def unpad(data):
    return data.rstrip(b'\x00').rstrip(b'\x80')
plaintext = b"HELLO_AES_BLOCK_CIPHER"
key = get_random_bytes(16)
iv = get_random_bytes(16)
padded = pad(plaintext)

# ---------- ECB MODE ----------
cipher_ecb = AES.new(key, AES.MODE_ECB)
ciphertext_ecb = cipher_ecb.encrypt(padded)
decrypted_ecb = unpad(cipher_ecb.decrypt(ciphertext_ecb))

# ---------- CBC MODE ----------
cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
ciphertext_cbc = cipher_cbc.encrypt(padded)
decipher_cbc = AES.new(key, AES.MODE_CBC, iv)
decrypted_cbc = unpad(decipher_cbc.decrypt(ciphertext_cbc))

# ---------- CFB MODE ----------
cipher_cfb = AES.new(key, AES.MODE_CFB, iv)
ciphertext_cfb = cipher_cfb.encrypt(padded)
decipher_cfb = AES.new(key, AES.MODE_CFB, iv)
decrypted_cfb = unpad(decipher_cfb.decrypt(ciphertext_cfb))
print("Plaintext:         ", plaintext)
print("\n--- ECB Mode ---")
print("Ciphertext (ECB): ", ciphertext_ecb)
print("Decrypted (ECB):  ", decrypted_ecb)

print("\n--- CBC Mode ---")
print("Ciphertext (CBC): ", ciphertext_cbc)
print("Decrypted (CBC):  ", decrypted_cbc)

print("\n--- CFB Mode ---")
print("Ciphertext (CFB): ", ciphertext_cfb)
print("Decrypted (CFB):  ", decrypted_cfb)

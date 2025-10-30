from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BS = 16

def pad(data):
    pad_len = BS - (len(data) % BS)
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    return data[:-data[-1]]

def flip_bit(data, bit_index):
    """Flip one bit in bytes (simulate error)."""
    b = bytearray(data)
    byte_i, bit_i = divmod(bit_index, 8)
    b[byte_i] ^= (1 << bit_i)
    return bytes(b)

def encrypt_ecb(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext))

def decrypt_ecb(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext))

def encrypt_cbc(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext))

def decrypt_cbc(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))

key = get_random_bytes(16)
iv  = get_random_bytes(16)

plaintext = b"This is a simple message for ECB and CBC mode demo!!"
print("Original plaintext:", plaintext)

ecb_ct = encrypt_ecb(key, plaintext)
cbc_ct = encrypt_cbc(key, plaintext, iv)

ecb_ct_err = flip_bit(ecb_ct, 8) 
cbc_ct_err = flip_bit(cbc_ct, 8)

try:
    dec_ecb_err = decrypt_ecb(key, ecb_ct_err)
    print("\nECB decrypted (error in C1):", dec_ecb_err)
except:
    print("\nECB decrypted: padding error (block damaged)")

try:
    dec_cbc_err = decrypt_cbc(key, cbc_ct_err, iv)
    print("\nCBC decrypted (error in C1):", dec_cbc_err)
except:
    print("\nCBC decrypted: padding error (block damaged)")

print("\n=== Error Propagation Analysis ===")
print("ECB: Error in ciphertext C1 -> only plaintext block P1 is affected.")
print("CBC: Error in ciphertext C1 -> corrupts P1 (completely) and P2 (one bit flipped).")
print("Beyond P2, plaintext is unaffected.")
print("\nIf there is a bit error in P1 before encryption:")
print("  -> In ECB: only C1 changes.")
print("  -> In CBC: both C1 and C2 change, as P1 affects C2 through chaining.")

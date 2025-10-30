from Crypto.Cipher import DES, DES3
from Crypto.Random import get_random_bytes
import time

def pad(data): 
    pad_len = 8 - len(data) % 8
    return data + bytes([pad_len]) * pad_len

plaintext = b"Meet me at the secret location at ten o'clock tonight!"

key_des = get_random_bytes(8)
iv_des = get_random_bytes(8)
cipher_des = DES.new(key_des, DES.MODE_CBC, iv_des)
start = time.time()
ct_des = cipher_des.encrypt(pad(plaintext))
end = time.time()


key_3des = DES3.adjust_key_parity(get_random_bytes(24))
iv_3des = get_random_bytes(8)
cipher_3des = DES3.new(key_3des, DES3.MODE_CBC, iv_3des)
start3 = time.time()
ct_3des = cipher_3des.encrypt(pad(plaintext))
end3 = time.time()

print("\n===== CBC ENCRYPTION RESULTS =====")
print("DES Ciphertext :", ct_des.hex().upper())
print("3DES Ciphertext:", ct_3des.hex().upper())
print(f"\nDES Encryption Time  : {end - start:.6f} sec")
print(f"3DES Encryption Time : {end3 - start3:.6f} sec")

print("\n===== ANALYSIS =====")
print("a) For SECURITY  : 3DES is stronger (168-bit key vs 56-bit DES).")
print("b) For PERFORMANCE: DES is faster (fewer rounds, smaller key).")

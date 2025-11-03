from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import sys

BLOCK_SIZE = 8


def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(p: bytes) -> bytes:
    if not p:
        raise ValueError("Input is empty")
    pad_len = p[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding")
    if p[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid padding")
    return p[:-pad_len]


def des_encrypt_ecb(key8: bytes, plaintext: bytes) -> bytes:
    """Encrypt in ECB mode. key8 must be 8 bytes."""
    if len(key8) != 8:
        raise ValueError("DES key must be exactly 8 bytes")
    cipher = DES.new(key8, DES.MODE_ECB)
    pt_padded = pkcs7_pad(plaintext)
    return cipher.encrypt(pt_padded)


def des_decrypt_ecb(key8: bytes, ciphertext: bytes) -> bytes:
    if len(key8) != 8:
        raise ValueError("DES key must be exactly 8 bytes")
    cipher = DES.new(key8, DES.MODE_ECB)
    pt_padded = cipher.decrypt(ciphertext)
    return pkcs7_unpad(pt_padded)


def des_encrypt_cbc(key8: bytes, iv8: bytes, plaintext: bytes) -> bytes:
    """Encrypt in CBC mode. iv8 must be 8 bytes."""
    if len(key8) != 8 or len(iv8) != 8:
        raise ValueError("Key and IV must be exactly 8 bytes")
    cipher = DES.new(key8, DES.MODE_CBC, iv=iv8)
    pt_padded = pkcs7_pad(plaintext)
    return cipher.encrypt(pt_padded)


def des_decrypt_cbc(key8: bytes, iv8: bytes, ciphertext: bytes) -> bytes:
    if len(key8) != 8 or len(iv8) != 8:
        raise ValueError("Key and IV must be exactly 8 bytes")
    cipher = DES.new(key8, DES.MODE_CBC, iv=iv8)
    pt_padded = cipher.decrypt(ciphertext)
    return pkcs7_unpad(pt_padded)


def demo():
    key = get_random_bytes(8)
    iv = get_random_bytes(8)

    plaintext = b"DES demo: The quick brown fox jumps over the lazy dog"
    print("Plaintext:", plaintext)
    c_ecb = des_encrypt_ecb(key, plaintext)
    p_ecb = des_decrypt_ecb(key, c_ecb)
    print("\nECB Mode:")
    print(" Key (hex):", key.hex())
    print(" Ciphertext (hex):", c_ecb.hex())
    print(" Decrypted:", p_ecb)
    c_cbc = des_encrypt_cbc(key, iv, plaintext)
    p_cbc = des_decrypt_cbc(key, iv, c_cbc)
    print("\nCBC Mode:")
    print(" Key (hex):", key.hex())
    print(" IV  (hex):", iv.hex())
    print(" Ciphertext (hex):", c_cbc.hex())
    print(" Decrypted:", p_cbc)
    if len(sys.argv) >= 2:
        try:
            user_key = bytes.fromhex(sys.argv[1])
            if len(user_key) != 8:
                raise ValueError
        except Exception:
            print("\nIf supplying a key, provide exactly 16 hex characters (8 bytes).")
            return
        print("\nUsing user-supplied key (ECB):", user_key.hex())
        ct = des_encrypt_ecb(user_key, plaintext)
        print(" Ciphertext:", ct.hex())
        print(" Decrypted:", des_decrypt_ecb(user_key, ct))


if __name__ == "__main__":
    demo()

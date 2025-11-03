import random
import string

def encrypt_vigenere_otp(plaintext, key_stream):
    ciphertext = ""
    for i, ch in enumerate(plaintext.upper()):
        if ch in string.ascii_uppercase:
            shift = key_stream[i]
            c = chr(((ord(ch) - 65 + shift) % 26) + 65)
            ciphertext += c
        else:
            ciphertext += ch
    return ciphertext

def decrypt_vigenere_otp(ciphertext, key_stream):
    plaintext = ""
    for i, ch in enumerate(ciphertext):
        if ch in string.ascii_uppercase:
            shift = key_stream[i]
            p = chr(((ord(ch) - 65 - shift) % 26) + 65)
            plaintext += p
        else:
            plaintext += ch
    return plaintext

if __name__ == "__main__":
    plaintext = "HELLOWORLD"
    key_stream = [random.randint(0, 25) for _ in plaintext]
    ciphertext = encrypt_vigenere_otp(plaintext, key_stream)
    decrypted = decrypt_vigenere_otp(ciphertext, key_stream)
    print("Plaintext:", plaintext)
    print("Key stream:", key_stream)
    print("Ciphertext:", ciphertext)
    print("Decrypted:", decrypted)

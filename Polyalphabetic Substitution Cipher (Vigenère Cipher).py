def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key = key.upper()
    j = 0
    for c in plaintext.upper():
        if c.isalpha():
            shift = ord(key[j % len(key)]) - ord('A')
            ciphertext += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
            j += 1
        else:
            ciphertext += c
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key = key.upper()
    j = 0
    for c in ciphertext.upper():
        if c.isalpha():
            shift = ord(key[j % len(key)]) - ord('A')
            plaintext += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
            j += 1
        else:
            plaintext += c
    return plaintext

plaintext = input("Enter plaintext: ")
key = input("Enter key: ")
ciphertext = vigenere_encrypt(plaintext, key)
print("Ciphertext:", ciphertext)
print("Decrypted:", vigenere_decrypt(ciphertext, key))

import string

def monoalphabetic_encrypt(plaintext, key):
    alphabet = string.ascii_lowercase
    table = str.maketrans(alphabet, key)
    return plaintext.lower().translate(table)

def monoalphabetic_decrypt(ciphertext, key):
    alphabet = string.ascii_lowercase
    table = str.maketrans(key, alphabet)
    return ciphertext.lower().translate(table)

key = "QWERTYUIOPASDFGHJKLZXCVBNM".lower()
plaintext = input("Enter plaintext: ")
ciphertext = monoalphabetic_encrypt(plaintext, key)
print("Ciphertext:", ciphertext)
print("Decrypted:", monoalphabetic_decrypt(ciphertext, key))

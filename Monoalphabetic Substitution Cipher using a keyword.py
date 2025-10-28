import string

def generate_cipher_alphabet(keyword):
    keyword = "".join(sorted(set(keyword.upper()), key=keyword.index))
    alphabet = string.ascii_uppercase
    cipher = keyword
    for c in alphabet:
        if c not in cipher:
            cipher += c
    return cipher

def monoalphabetic_encrypt(plaintext, cipher):
    alphabet = string.ascii_uppercase
    result = ""
    for ch in plaintext.upper():
        if ch.isalpha():
            result += cipher[alphabet.index(ch)]
        else:
            result += ch
    return result

def monoalphabetic_decrypt(ciphertext, cipher):
    alphabet = string.ascii_uppercase
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += alphabet[cipher.index(ch)]
        else:
            result += ch
    return result

keyword = "CIPHER"
cipher_alphabet = generate_cipher_alphabet(keyword)
print("Plain:  ", " ".join(string.ascii_lowercase))
print("Cipher: ", " ".join(cipher_alphabet))

plaintext = input("Enter plaintext: ")
ciphertext = monoalphabetic_encrypt(plaintext, cipher_alphabet)
print("Ciphertext:", ciphertext)
print("Decrypted:", monoalphabetic_decrypt(ciphertext, cipher_alphabet))

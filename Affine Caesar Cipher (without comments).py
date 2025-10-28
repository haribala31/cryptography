import math

def mod_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def affine_encrypt(plaintext, a, b):
    result = ""
    for char in plaintext.upper():
        if char.isalpha():
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        else:
            result += char
    return result

def affine_decrypt(ciphertext, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "Decryption not possible (a not invertible mod 26)"
    for char in ciphertext.upper():
        if char.isalpha():
            result += chr(((a_inv * ((ord(char) - 65) - b)) % 26) + 65)
        else:
            result += char
    return result

a = int(input("Enter value of a: "))
b = int(input("Enter value of b: "))
plaintext = input("Enter plaintext: ")

if math.gcd(a, 26) != 1:
    print("Invalid key: 'a' must be coprime with 26.")
else:
    cipher = affine_encrypt(plaintext, a, b)
    print("Ciphertext:", cipher)
    print("Decrypted:", affine_decrypt(cipher, a, b))
